import datetime

import requests
from bs4 import BeautifulSoup

from registry.models import GradeIdLink
from util import get_school_year


def get_practice_exam_data(birth_year, month, school):
    """get_practice_exam_data

        全県模試のネットサポートサイトから、模試のデータを取得する

        Args:
            birth_year(str): 生徒が生まれた年
            month (str): '7', '8', '10', '12', '1', '3' のいずれか(模試の実施月は変更の可能性あり)
            school(str): 'hashido', 'seya', 'yamato', 'honko' のいずれか

        Returns:
            student_list(list): 生徒の模試データ(dict)を格納したリスト
    """

    today = datetime.date.today()
    if today.month == 4:
        # 現在が４月の場合は、一つ前の年度のデータを取得する
        this_year = get_school_year() - 1
    else:
        this_year = get_school_year()

    birth_years = {
        'third': GradeIdLink.objects.get(grade='中３').birth_year,
        'second': GradeIdLink.objects.get(grade='中２').birth_year,
        'first': GradeIdLink.objects.get(grade='中１').birth_year,
    }

    # メールアドレスとパスワードの指定
    if school == 'hashido':
        USER_ID = "ZEN06128001"
        PASS = "nRmdneA2"
    elif school == 'seya':
        USER_ID = "ZEN06128002"
        PASS = "7YCFrGRr"
    elif school == 'yamato':
        USER_ID = "ZEN11128003"
        PASS = "2hCTFbgn"

    # 実施回の取得(exam_timeは全県模試の実施回)
    if month == '7':  # ７月
        exam_time = '2'
    elif month == '8':  # ８月
        if birth_year == str(birth_years['third']):
            exam_time = '3'
        elif birth_year == str(birth_years['second']) or birth_year == str(birth_years['first']):
            exam_time = '1'
    elif month == '10':  # 10月
        exam_time = '5'  # ここは今後変更になるかも(第５回は10月下旬実施回)
    elif month == '12':  # 12月
        if birth_year == str(birth_years['third']):
            exam_time = '6'
        elif birth_year == str(birth_years['second']) or birth_year == str(birth_years['first']):
            exam_time = '2'
    elif month == '1':  # 1月
        exam_time = '7'
    elif month == '3':  # 3月
        exam_time = '3'

    # セッションを開始
    session = requests.session()
    response = session.get("https://www.kks-zenken.jp/index.aspx")

    # BeautifulSoupオブジェクト作成(token取得の為)
    bs = BeautifulSoup(response.text, 'html.parser')

    # html要素からログインに必要なデータを取得
    viewState = bs.find(attrs={'name': '__VIEWSTATE'}).get('value')
    eventValidation = bs.find(attrs={'name': '__EVENTVALIDATION'}).get('value')

    # ログインに必要なデータ
    login_data = {
        'ctl00$txt_user': USER_ID,
        'ctl00$txt_pass': PASS,
        '__VIEWSTATEGENERATOR': '90059987',
        '__VIEWSTATE': viewState,
        '__EVENTVALIDATION': eventValidation,
        '__EVENTTARGET': 'ctl00$btn_login',
        '__EVENTARGUMENT': '',
    }

    # action
    url_login = "https://www.kks-zenken.jp/index.aspx"
    res = session.post(url_login, data=login_data)
    res.raise_for_status()  # エラーならここで例外を発生させる

    # 教師用閲覧資料へ
    res = session.get('https://www.kks-zenken.jp/paper/teacher/index.aspx')
    res.raise_for_status()

    # # 生徒コード順へ
    # birth_year = '2006'
    # this_year = '2019'
    # times = '3'

    url = 'https://www.kks-zenken.jp/paper/teacher/seitoCodeList.aspx?210&{}&{}&{}'.format(birth_year,
                                                                                           this_year,
                                                                                           exam_time)
    res = session.get(url)
    res.raise_for_status()
    # ここまでで教師用閲覧データが手に入ったので、以下で必要なデータを取得していく

    # データの取得
    soup = BeautifulSoup(res.text, "html.parser")
    label_num_list = ['7', '15', '25', '73', '31', '32', '34', '35', '37', '38', '40',
                      '41', '43', '44', '46', '47', '49', '50']

    key_list = ['name', 'first_choice', 'second_choice', 'third_choice', 'english_score', 'english_deviation',
                'math_score', 'math_deviation', 'japanese_score', 'japanese_deviation', 'science_score',
                'science_deviation', 'social_score', 'social_deviation', 'sum_three', 'dev_three', 'sum_all', 'dev_all']

    # ループカウントの取得(ページの'No'を取得していく)
    i = 0
    while True:
        try:
            num = soup.find(id="cph_main_SeitocodelistDG_Label5_{}".format(str(i))).string
            loop_count = int(num)
            i += 1
        except AttributeError:
            break

    if i == 0:
        return False

    # 生徒の辞書を作り、key_listのキーに１つずつ値をセット。
    # そのあと student_list に入れていく
    student_list = []
    for i in range(loop_count):
        student = {}
        for j in range(len(label_num_list)):
            try:
                student[key_list[j]] = soup.find(id="cph_main_SeitocodelistDG_Label{}_{}".format(label_num_list[j], i))\
                    .string.replace('\u3000', ' ').strip('['']').strip()
            except AttributeError:
                break
        student_list.append(student)

    return student_list
