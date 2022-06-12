from urllib.parse import urlencode

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse

from app_base import *
from download.pdf_name_sheet import delete_files
from student.models import Student
from util import convert_school
from util import convert_grade
from zenken.csv import make_csv
from zenken.logic import cities
from zenken.logic import zenken_create_or_update
from zenken.models import Zenken
from zenken.zenken_delivery import ZenkenDelivery

logger = getLogger(__name__)


@login_required(login_url='login/')
def zenken_top(request):
    url = request.path
    context = {}
    # POSTリクエストの場合、全県の登録情報が送られてくるので、DBへ登録し、top画面を返す
    if request.method == 'POST':
        data = dict(request.POST)
        # logic.py の zenken_create_or_update で登録を実行する
        logger.info(f'全県模試データ登録・更新 開始 (user:{request.user})')
        result = zenken_create_or_update(data)
        if result:
            logger.info(f'全県模試データ登録・更新 完了 (user:{request.user})')
            messages.success(request, '全県模試データを登録・更新しました')
        else:
            logger.info(f'全県模試データ登録・更新 失敗 (user:{request.user})')
            messages.error(request, '全県模試データを登録・更新できませんでした')

        redirect_url = reverse('zenken:top')
        parameters = urlencode({'school': data['school'][0], 'grade': data['grade'][0]})
        url = f'{redirect_url}?{parameters}'
        return redirect(url)

    # GETリクエストの場合
    if 'school' in request.GET:
        context['cities'] = cities()  # ドロップダウンリスト生成用
        context['school'] = request.GET.get('school')
        context['grade'] = request.GET.get('grade')

        # schoolとgradeを日本語に変換しておく
        converted_school = convert_school(context['school'])
        converted_grade = convert_grade(context['grade'])

        students = Student.objects.filter(
            school=converted_school, grade=converted_grade, id__gte=0).order_by('id')
        context['students'] = []
        for student in students:
            # Zenken がない場合がある(入塾して初めての模試の場合など)
            zenken_db_data = Zenken.objects.filter(student_id=student.id).first()
            if zenken_db_data:
                zenken = ZenkenDelivery(student, zenken_db_data)
            else:
                zenken = ZenkenDelivery(student)
            context['students'].append(zenken)
        # 模試番号順に並び替える
        context['students'] = sorted(context['students'], key=lambda z: (z.number is None, z.number))
        # edit でGETリクエストがあった場合は zenken_edit.html へ context を送る
        if 'edit' in url:
            return render(request, 'zenken/zenken_edit.html', context)

        # ダウンロードの場合は、ファイルを作成したあと、ダウンロードし、そのファイルを削除する
        if 'download' in url:
            # csvファイルの作成・ダウンロード
            file_name = make_csv(converted_school, converted_grade, students)

            # # ダウンロード
            # logger.info(f'全県模試登録用CSV({converted_school}{converted_grade})ダウンロード〔user: {request.user}〕')
            # content_type = 'text/csv'
            # response = HttpResponse(open(file_name, 'rb').read(), content_type=content_type)
            # response['Content-Disposition'] = 'attachment; filename=' + file_name
            # # delete_files('*.csv')  # ファイルの削除
            # return response

    return render(request, 'zenken/zenken_top.html', context)
