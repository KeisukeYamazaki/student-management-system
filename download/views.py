import shutil

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render

from app_base import *
from download.excel_meeting_sheet import make_excel_meeting_sheet
from download.pdf_name_sheet import count_up
from download.pdf_name_sheet import merge_pdf_in_dir
from download.pdf_name_sheet import delete_files
from download.pdf_name_sheet import make_pdf_name_sheets
from download.excel_name_sheet import make_excel_name_sheet
from registry.models import SchoolRecord
from registry.models import RegularExam
from registry.models import PracticeExam
from student.exam_record import ExamRecord
from student.models import make_future_path
from student.models import HomeRoom
from student.models import FuturePath
from student.models import PublicHighSchool
from student.models import PrivateHighSchool
from student.models import Student
from student.update_futurepath import update_or_create_future_path
from util import convert_grade
from util import katakana_to_romaji


logger = getLogger(__name__)


@login_required(login_url='login/')
def download_home(request):
    return render(request, 'download/download.html')


@login_required(login_url='login/')
def meeting_sheet_view(request, **kwargs):
    context = {'meeting_sheet': 'meeting_sheet'}

    # POSTのリクエストは「そのままダウンロード」と「編集してダウンロード」の2種類
    if request.method == 'POST':
        logger.info('編集してダウンロード')
        data_dict = request.POST.dict()
        # もしPOSTされたデータに志望校が入っていたら、編集されたデータ。登録を行う。
        if 'first_choice' in data_dict:
            # 編集されたものを登録する
            future_path = FuturePath.objects.filter(student_id=data_dict['id']).first()
            logger.info(f'進路情報:{future_path.to_string()}')
            student = Student.objects.get(id=data_dict['id'])
            logger.info(f'生徒情報:{student.to_string()}')
            # future_pathデータがあれば、更新、なければ新規登録
            result = update_or_create_future_path(student, future_path, data_dict)
            if result:
                logger.info(f'進路情報登録・更新：{student.last_name} {student.first_name}〔user: {request.user}〕')
            else:
                logger.info(f'進路情報登録・更新 失敗：{student.last_name} {student.first_name}〔user: {request.user}〕')

        # ダウンロード処理の開始
        student = Student.objects.get(id=int(data_dict['id']))
        exam_record = ExamRecord(student)
        try:
            # 学年のよって以下を取得
            # 1. 成績・定期試験結果を取得するループの回数
            # 2. 前年度最後の模試結果
            if student.grade == '中１':
                loop_count = 1
                # 中１は前年度の模試結果は存在しないのでNone
                last_grade_exam = None
            elif student.grade == '中２':
                loop_count = 2
                # 前年度の模試結果が無い場合は例外処理
                last_grade_exam = PracticeExam.objects.get(student_id=student.id, grade='中１', month_id=6)
            elif student.grade == '中３':
                loop_count = 3
                # 前年度の模試結果が無い場合は例外処理
                last_grade_exam = PracticeExam.objects.get(student_id=student.id, grade='中２', month_id=6)
        except ObjectDoesNotExist:
            last_grade_exam = None

        # ファイル名の生成
        romaji_name = katakana_to_romaji(f'{student.last_ruby}{student.first_ruby}')
        file_name = today.strftime('%Y%m%d') + f'{romaji_name}.xlsx'

        # 当該生徒の成績と定期試験の結果を格納するリスト
        record_list = []
        r_exam_list = []

        # 各学年の成績と定期試験結果をリストに格納していく
        grades = ['中１', '中２', '中３']
        for i in range(loop_count):
            record_list.append(SchoolRecord.objects.filter(student_id=student.id, grade=grades[i]).order_by('id'))
            r_exam_list.append(RegularExam.objects.filter(student_id=student.id, grade=grades[i]).order_by('id'))
        # i は上のループの最終になるので、ここでgradesは当該の学年になる
        this_grade_exam_list = PracticeExam.objects.filter(student_id=student.id, grade=grades[i]).order_by('id')

        # future_path を取得する
        try:
            future_path = FuturePath.objects.get(student_id=student.id)
        except ObjectDoesNotExist:
            # もしfuture_pathが存在しなければ、ここで作りそれを取得する
            logger.info('進路情報がないため進路情報新規作成')
            make_future_path(student.id)
            future_path = FuturePath.objects.get(student_id=student.id)

        # public_school, private_school, ともに下記のような辞書を取得
        # {'first': 第一志望高校, 'second': 第二志望高校, 'third': 第三志望高校 }
        public_school_dict = future_path.get_public_schools()
        private_school_dict = future_path.get_private_schools()

        # 追加の私立高校があれば、辞書に加える
        if 'private_school4' in data_dict:
            private_school_dict['fourth'] = PrivateHighSchool.objects.get(id=data_dict['private_school4'])
        if 'private_school5' in data_dict:
            private_school_dict['fifth'] = PrivateHighSchool.objects.get(id=data_dict['private_school5'])

        # 公立高校のデータを取得する
        calc_score_dict_list = []
        score_dict_list = []
        keys = ['first', 'second', 'third']
        for i in range(3):
            # 第1 〜 第3志望の高校を取得
            public_school = public_school_dict[keys[i]]
            if public_school:
                # 直近の高校入試のデータと、3年間の平均のデータを取得する
                # score_dict {str:{}} - {'ave'or'late': {record: 平均内申, score: 平均入試点数, border: ボーダー点数}}
                # score_dict_list は score_dictを格納したリスト
                score_dict_list.append(public_school.get_data_all_kind())
                if not exam_record.four_five == '':
                    # /45があれば、現在の成績と志望校のギャップを計算したものを取得する
                    calc_score_dict_list.append(public_school.get_data_all_kind(exam_record))
                else:
                    # なければ空の辞書を追加（数値データと志望順と対応させるため）
                    calc_score_dict_list.append({})

        logger.info('面談シート作成関数呼び出し')
        make_excel_meeting_sheet(file_name,
                                 student,
                                 record_list,
                                 r_exam_list,
                                 this_grade_exam_list,
                                 last_grade_exam,
                                 public_school_dict,
                                 calc_score_dict_list,
                                 score_dict_list,
                                 private_school_dict)
        # ダウンロード
        logger.info(f'面談シート({student.last_name} {student.first_name})ダウンロード〔user: {request.user}〕')
        content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response = HttpResponse(open(file_name, 'rb').read(), content_type=content_type)
        response['Content-Disposition'] = 'attachment; filename=' + file_name
        delete_files('*.xlsx')  # ファイルの削除
        return response

    if 'pk' in kwargs:
        logger.info('面談シートに記載する進路情報の編集画面')
        logger.info(f'ID:{kwargs["pk"]}')
        context['grade'] = kwargs['grade']
        logger.info(f'学年：{context["grade"]}')
        context['student_data'] = Student.objects.get(id=kwargs['pk'])
        logger.info(f'生徒情報：{context["student_data"].to_string()}')
        context['exam_record'] = ExamRecord(context['student_data'])
        logger.info(f'試験結果情報取得')
        # future_path を取得する
        try:
            context['future_path'] = FuturePath.objects.get(student_id=kwargs['pk'])
        except ObjectDoesNotExist:
            # もしfuture_pathが存在しなければ、ここで作りそれを取得する
            logger.info('進路情報が存在しないため進路情報新規作成')
            make_future_path(kwargs['pk'])
            context['future_path'] = FuturePath.objects.get(student_id=kwargs['pk'])
        logger.info(f'進路情報：{context["future_path"].to_string()}')
        context['public_high_schools'] = PublicHighSchool.objects.all()
        logger.info('公立高校情報取得')
        context['private_high_schools'] = PrivateHighSchool.objects.all()
        logger.info('私立高校情報取得')
        return render(request, 'download/download.html', context)

    if kwargs:
        grade = convert_grade(kwargs['grade'])
        context['grade'] = kwargs['grade']
        context['students'] = Student.objects.filter(grade=grade, id__gte=0).order_by('home_room', 'id')

    return render(request, 'download/download.html', context)


@login_required(login_url='login/')
def name_sheet_view(request, **kwargs):
    if request.method == 'POST':
        data_dict = dict(request.POST)
        if data_dict['file_type'][0] == 'pdf':
            count = count_up()
            for home_room in data_dict['class_name']:
                students = Student.objects.filter(home_room=home_room, id__gt=0)
                name = 'sheet' + str(count.__next__()) + '.pdf'
                make_pdf_name_sheets(name, home_room, students)
                shutil.copy(base_path + '/' + name, base_path + '/' + 'sheet' + str(count.__next__()) + '.pdf')

            file_name = today.strftime('%Y%m%d') + 'name_sheet.pdf'
            merge_pdf_in_dir(file_name)

            # ダウンロード
            logger.info(f'中学生名簿ダウンロード(pdf)〔user: {request.user}〕')
            response = HttpResponse(open(file_name, 'rb').read(), content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename=' + file_name
            delete_files('*.pdf')  # ファイルの削除
            return response

        if data_dict['file_type'][0] == 'excel':
            dict_home_room_students = {}
            for home_room in data_dict['class_name']:
                dict_home_room_students[home_room] = Student.objects.filter(home_room=home_room, id__gt=0)
            file_name = today.strftime('%Y%m%d') + 'name_sheet.xlsx'
            make_excel_name_sheet(file_name, dict_home_room_students)

            # ダウンロード
            logger.info(f'中学生名簿ダウンロード(excel)〔user: {request.user}〕')
            content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            response = HttpResponse(open(file_name, 'rb').read(), content_type=content_type)
            response['Content-Disposition'] = 'attachment; filename=' + file_name
            delete_files('*.xlsx')  # ファイルの削除
            return response

    if kwargs:
        context = {'kind': kwargs['kind']}
        if kwargs['kind'] == 'junior':
            context['grade_list'] = ['中３', '中２', '中１']
            context['home_rooms'] = HomeRoom.objects.filter(grade__startswith='中')

        else:
            context['grade_list'] = ['小６', '小５', '小４', '小３']
            context['home_rooms'] = HomeRoom.objects.filter(grade__startswith='小')

        context['students'] = {}
        for home_room in context['home_rooms']:
            context['students'][home_room.name] = Student.objects.filter(home_room=home_room.name, id__gt=0)
        return render(request, 'download/download.html', context)

    return render(request, 'download/download.html')
