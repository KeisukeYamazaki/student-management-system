from urllib.parse import urlencode

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse

from app_base import *
from registry.google import regular_registry_by_google
from registry.practice_exam import get_practice_exam_data
from student.models import Student
from student.models import JuniorHighSchool
from util import convert_grade
from util import get_school_year
from registry.logic import school_record_create_or_update
from registry.logic import regular_exam_create_or_update
from registry.logic import practice_exam_create_or_update
from registry.logic import register_from_zenken
from registry.logic import get_record_school_year
from registry.models import GradeIdLink
from registry.models import TimeLimit
from registry.models import SchoolRecord
from registry.models import RegularExam
from registry.models import PracticeExam
from registry.sql import get_school_records

logger = getLogger(__name__)

terms = {
    1: '１学期・前期',
    2: '２学期',
    3: '３学期・後期',
    4: '２学期・後期',
}


@login_required(login_url='login/')
def registry_home(request):
    return render(request, 'registry/registry.html')


@login_required(login_url='login/')
def registry_school_record(request):
    if request.method == 'POST':
        # request.POSTがQueryDictとして渡されている
        registry_data = dict(request.POST)
        school_record_create_or_update(registry_data)

        now_grade = convert_grade(request.GET.get("now"))
        change_grade = convert_grade(request.GET.get("grade"))
        term_name = terms[int(request.GET.get("term"))]

        messages.success(request, f'現{now_grade}の{change_grade}・{term_name}の成績を更新しました')
        logger.info(f'成績更新処理：現{now_grade}-{change_grade}_{term_name}〔user: {request.user}〕')

        redirect_url = reverse('registry:school-record')
        parameters = urlencode({
            'now': request.GET.get("now"),
            'grade': request.GET.get("grade"),
            'term': request.GET.get("term"),
        })
        url = f'{redirect_url}?{parameters}'
        return redirect(url)

    if "now" in request.GET:
        context = {
            'now': request.GET.get("now"),
            'grade': request.GET.get("grade"),
            'large_grade': convert_grade(request.GET.get("grade")),
            'term_num': request.GET.get("term"),
            'term': terms[int(request.GET.get("term"))],
        }

        context['year'] = get_record_school_year(context['now'], context['grade'])

        context['objects'] = get_school_records(
            convert_grade(context['now']),
            convert_grade(context['grade']),
            context['term'],
        )

        return render(request, 'registry/registry_school_record.html', context)

    return render(request, 'registry/registry_school_record.html')


@login_required(login_url='login/')
def registry_practice_exam(request, **kwargs):
    context = {}
    if kwargs:
        context['kind'] = kwargs['kind']
        context['third_grade_birth_year'] = GradeIdLink.objects.get(grade='中３').birth_year
        context['second_grade_birth_year'] = GradeIdLink.objects.get(grade='中２').birth_year
        context['first_grade_birth_year'] = GradeIdLink.objects.get(grade='中１').birth_year

    if request.method == 'POST':
        post_data = request.POST.dict()
        practice_data = request.session['practice_data']
        # 月の名前の数字で入っている(7, 8, 10, 12, 1, 3 いずれか)
        month = post_data['month']
        grade = GradeIdLink.objects.get(birth_year=post_data['birth_year']).grade
        exam_year = get_school_year() if datetime.date.today().month != 4 else get_school_year() - 1
        # ここで登録処理を実施。resultはTrueかFalse。
        result = register_from_zenken(practice_data, grade, exam_year, month)
        # セッションを削除しておく
        request.session['practice_data'] = ''

        # のちのログ、メッセージで使用する校舎名はここで代入しておく
        if request.GET.get('school') == 'hashido':
            school_name = '橋戸校'
        elif request.GET.get('school') == 'seya':
            school_name = '瀬谷校'
        elif request.GET.get('school') == 'yamato':
            school_name = '大和校'
        elif request.GET.get('school') == 'honko':
            school_name = '本校'

        if result[0]:
            logger.info('模試データの登録処理:{}{} {}年度 {}月実施 〔user: {}〕'.format(
                school_name, grade, str(exam_year), month, request.user))
            messages.success(request, '{}{} {}年度 {}月実施の模試結果を登録しました'.format(
                school_name, grade, str(exam_year), month))
            if len(result[1]) != 0:
                messages.error(request, '{} は登録できませんでした'.format(', '.join(result[1])))
        else:
            messages.error(request, '模試データの登録に失敗しました')
            logger.error('[登録失敗] 登録:{}{} {}年度 {}月実施模試 〔user: {}〕'.format(
                school_name, grade, str(exam_year), month, request.user))

        return redirect('registry:practice-exam', kind='zenken')

    if 'birth_year' in request.GET:
        birth_year = request.GET.get('birth_year')
        # テンプレートの比較のためにintにしておく
        context['birth_year'] = int(birth_year)
        # 変数としても、テンプレートに送るのにも使うので二重に代入している
        month = context['month'] = request.GET.get('month')
        school = context['school'] = request.GET.get('school')

        # [{},{},,,] の形式で送られてくる。セッションにも格納。
        if get_practice_exam_data(birth_year, month, school):
            context['practice_data'] = get_practice_exam_data(birth_year, month, school)
            request.session['practice_data'] = get_practice_exam_data(birth_year, month, school)
        else:
            # 生徒が１人もいなかった場合
            messages.error(request, '生徒が存在しません')
            return render(request, 'registry/registry_practice_exam.html', context)

        logger.info(f'模試データの取得:〔user: {request.user}〕')
        logger.info(context['practice_data'])

        return render(request, 'registry/registry_practice_exam.html', context)

    return render(request, 'registry/registry_practice_exam.html', context)


@login_required(login_url='login/')
def registry_personal(request, **kwargs):
    context = {}

    if kwargs:
        grade = convert_grade(kwargs['grade'])
        context['grade'] = kwargs['grade']
        context['students'] = Student.objects.filter(grade=grade, id__gte=0).order_by('home_room', 'id')

    if 'pk' in kwargs:
        context['student'] = Student.objects.get(id=kwargs['pk'])

    if 'kind' in kwargs:
        id = context['student'].id
        context['term'] = JuniorHighSchool.objects.get(name=context['student'].local_school).term
        grade_list = ['中１', '中２', '中３']
        context['kind'] = kwargs['kind']
        context['count'] = 0
        if context['kind'] == 'school_record':
            # 当該生徒の全成績を取得
            context['school_records'] = {}
            for grade in grade_list:
                context['school_records'][grade] = SchoolRecord.objects.filter(student_id=id, grade=grade).order_by('id')
                context['count'] += len(context['school_records'][grade])
        elif context['kind'] == 'regular_exam':
            # 当該生徒の全定期試験結果を取得
            context['regular_exams'] = {}
            for grade in grade_list:
                context['regular_exams'][grade] = RegularExam.objects.filter(student_id=id, grade=grade).order_by('id')
                context['count'] += len(context['regular_exams'][grade])
        elif context['kind'] == 'practice_exam':
            # 当該生徒の全模試結果を取得
            context['practice_exams'] = {}
            for grade in grade_list:
                context['practice_exams'][grade] = PracticeExam.objects.filter(student_id=id, grade=grade).order_by(
                    'grade', 'month_id')
                context['count'] += len(context['practice_exams'][grade])

    if request.method == 'POST':
        registry_data = dict(request.POST)
        # メッセージ・ログ用のname, grade
        name = context['student'].last_name + context['student'].first_name
        grade = context['student'].grade
        if context['kind'] == 'school_record':
            # ここで成績の登録・更新を行う(logic.py:school_record_create_or_update)
            school_record_create_or_update(registry_data, personal=True)
            # メッセージの表示、ログの出力
            messages.success(request, f'{grade} {name} の成績を登録・更新しました')
            logger.info(f'個人[成績]登録処理 : {grade} {name} 〔user: {request.user}〕')
        elif context['kind'] == 'regular_exam':
            # ここで定期試験の登録・更新を行う(logic.py:regular_exam_create_or_update)
            regular_exam_create_or_update(registry_data, personal=True)
            messages.success(request, f'{grade} {name} の定期試験結果を登録・更新しました')
            logger.info(f'個人[定期試験]登録処理 : {grade} {name} 〔user: {request.user}〕')
        elif context['kind'] == 'practice_exam':
            # ここで定期試験の登録・更新を行う(logic.py:regular_exam_create_or_update)
            practice_exam_create_or_update(registry_data)
            messages.success(request, f'{grade} {name} の模試結果を登録・更新しました')
            logger.info(f'個人[模試]登録処理 : {grade} {name} 〔user: {request.user}〕')
        # リダイレクト
        return redirect('registry:personal', grade=kwargs['grade'], pk=kwargs['pk'], kind=kwargs['kind'])

    return render(request, 'registry/registry_personal.html', context)


@login_required(login_url='login/')
def registry_regular_exam(request):
    context = {}
    if request.method == 'POST':
        post_data = request.POST.dict()
        if post_data['button'] == 'registry':
            # 手動登録の場合(regular_registry_by_googleを実行すると登録した人数のメッセージが返ってくる)
            message = regular_registry_by_google(post_data['test_kind'])
            logger.info(f'定期試験手動登録:〔user: {request.user}〕')
            messages.success(request, message)
        if post_data['button'] == 'limit':
            # 自動登録期限設定の場合
            date = post_data['date'].replace('/', '-')
            limit = TimeLimit.objects.filter(id=1).first()
            # すでにある場合は更新し、そうでない場合は新規に作る(常にidは1)
            if limit:
                limit.id = 1
                limit.sheet_name = post_data['test_kind']
                limit.limit_date = date
                limit.save()
            else:
                limit = TimeLimit(
                    id=1,
                    sheet_name=post_data['test_kind'],
                    limit_date=date,
                )
                limit.save()
            logger.info(f'定期試験自動登録期限設定:期限-{post_data["date"]}〔user: {request.user}〕')
            messages.success(request, f'定期試験の自動登録期限を設定しました')

    # 自動登録設定があり、期限が過ぎていなければテンプレートに送る
    limit = TimeLimit.objects.filter(id=1).first()
    if limit:
        if limit.limit_date >= datetime.date.today():
            context['test_kind'] = limit.sheet_name
            context['limit_date'] = limit.limit_date

    return render(request, 'registry/registry_regular_exam.html', context)
