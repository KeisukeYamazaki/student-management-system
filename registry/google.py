import os
import pickle
from logging import getLogger

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from registry.logic import student_name_to_id
from registry.models import RegularExam
from student.models import Student
from student.models import JuniorHighSchool

from util import get_school_year

logger = getLogger(__name__)


# 学年の数(=中１〜３なので3 ※学年末は2)
GRADE_COUNT = 3
# 1学年分の列数
ONE_GRADE_COL = 29

# 各列の基準となる位置からの数値を定義
NUMBER_COL = 2
NAME_COL = 3
ENGLISH_COL = 16
MATH_COL = 17
JAPANESE_COL = 18
SCIENCE_COL = 19
SOCIAL_COL = 20
MUSIC_COL = 22
ART_COL = 23
PE_COL = 24
TECH_COL = 25
HOME_COL = 26

GRADE_LIST = ['中３', '中２', '中１']


def regular_registry_by_google(test_kind):
    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

    # シート取得のために実際の取得名に変換
    if test_kind == '１学期期末・前期中間':
        test_kind = '１学期定期試験'
    elif test_kind == '２学期中間・前期期末':
        test_kind = '２学期中間（９月）'
    elif test_kind == '２学期期末・後期中間':
        test_kind = '定期試験結果（11月）'

    # The ID and range of a sample spreadsheet.
    SPREADSHEET_ID = '1yv4tdu58uujjP-BYRQdwRFWejrPHrZbmK-PK6zkkFkY'
    RANGE_NAME = f'{test_kind}!A1:CK80'

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '/Users/apple/Dropbox/vnev_sms/sms/sms/registry/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # シートを取得し、値を二次元配列で取得
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=RANGE_NAME).execute()
    values = result.get('values', [])

    # 取得した二次元配列の行が85より少なければ、空白で埋めて85の長さにする
    LAST_COL = 85
    for row in values:
        if len(row) <= LAST_COL:
            for _ in range(LAST_COL - len(row)):
                row.append('')

    # 各学年の生徒を取得
    students = {}
    for grade in GRADE_LIST:
        students[grade] = Student.objects.filter(grade=grade, id__gt=0)

    # 各学年のデータを格納する辞書を生成('中３': [{}, {}, ...], '中２': ...)
    result_dict = {}
    for i in range(len(GRADE_LIST)):
        grade = GRADE_LIST[i]
        # get_one_grade_scoresメソッドで各学年の結果を取得
        result_dict[grade] = get_one_grade_scores(values, test_kind, i, students[grade], grade)

    # 生成したデータをもとにDBへ登録する(google_regular_create_or_updateメソッド)
    count = google_regular_create_or_update(result_dict)
    return f'{count}人の結果を登録しました'


def get_one_grade_scores(values, test_kind, loop_count, students, grade):
    """registry_one_grade_scores

        1学年分の定期試験データリストを返す

        Args:
            values(list[list]): シートの全データを含む2次元配列
            test_kind (str): テストの種類('１学期中間', '１学期期末・前期中間', '２学期中間・前期期末', '２学期期末・後期中間', '学年末')
            loop_count(int): ループカウント(0~2)
            students(list[Student]): Studentインスタンスを格納したリスト
            grade(str): 学年('中３', '中２', '中１')

        Returns:
            results(list): 1学年分の定期試験データリスト
    """
    # 生徒の結果を格納するリスト[data{}, data{}, ...]
    results = []
    # 列の最初の行を決める
    start_col = ONE_GRADE_COL * loop_count

    # DBに登録されている生徒の結果を登録できるように、当該学年の生徒名のリストを作る
    name_list = [f'{student.last_name} {student.first_name}' for student in students]

    # 変換された名前をもとに戻す
    if test_kind == '１学期定期試験':
        test_kind = '１学期期末・前期中間'
    elif test_kind == '２学期中間（９月）':
        test_kind = '２学期中間・前期期末'
    elif test_kind == '定期試験結果（11月）':
        test_kind = '２学期期末・後期中間'

    # 1クラス分の行数 × クラス数の数だけループする
    last_row = get_last_row(values, start_col)
    for i in range(last_row):
        # 行の配列の数が3以上なら処理を続ける
        if len(values[i]) >= start_col + NAME_COL + 1:
            # 姓名の間は半角スペースにしておく
            name = values[i][start_col + NAME_COL].replace('　', ' ')
            if name in name_list and is_registable(values[i], start_col):
                # リスト内に名前があった場合は値を取得してリストへ格納
                id = student_name_to_id(students, name)
                # idから生徒を取得
                student = Student.objects.get(id=id)
                term = JuniorHighSchool.objects.get(name=student.local_school).term
                # dataに1人分の生徒の結果を格納する
                data = {
                    'student_id': id,
                    'grade': grade,
                    'exam_year': get_school_year(),
                    'regular_id': get_test_id(test_kind, term),
                    'english': values[i][start_col + ENGLISH_COL],
                    'math': values[i][start_col + MATH_COL],
                    'japanese': values[i][start_col + JAPANESE_COL],
                    'science': values[i][start_col + SCIENCE_COL],
                    'social_studies': values[i][start_col + SOCIAL_COL],
                    'music': values[i][start_col + MUSIC_COL],
                    'art': values[i][start_col + ART_COL],
                    'pe': values[i][start_col + PE_COL],
                    'tech': values[i][start_col + TECH_COL],
                    'home': values[i][start_col + HOME_COL],
                }
                sum_five = sum([int_or_zero(data['english']),
                                int_or_zero(data['math']),
                                int_or_zero(data['japanese']),
                                int_or_zero(data['science']),
                                int_or_zero(data['social_studies'])])
                data['sum_five'] = sum_five
                results.append(data)
    return results


def get_test_id(test_kind, term):
    """get_test_id

        1学年分の定期試験データリストを返す

        Args:
            test_kind(str): テストの種類('１学期中間', '１学期期末・前期中間', '２学期中間・前期期末', '２学期期末・後期中間', '学年末')
            term (str): '３学期制', '２学期制' のいずれか

        Returns:
            regular_id(int): regular_id
    """
    if test_kind == '１学期中間':
        return 1
    if test_kind == '１学期期末・前期中間':
        if term == '３学期制':
            return 3
        if term == '２学期制':
            return 2
    if test_kind == '２学期中間・前期期末':
        if term == '３学期制':
            return 5
        if term == '２学期制':
            return 4
    if test_kind == '２学期期末・後期中間':
        if term == '３学期制':
            return 7
        if term == '２学期制':
            return 6
    if test_kind == '学年末':
        return 8


def int_or_zero(score):
    try:
        return int(score)
    except ValueError:
        return 0


def google_regular_create_or_update(result_dict):
    """google_regular_create_or_update

        定期試験データをDBへ登録する

        Args:
            result_dict(dict): 学年と結果のリストを格納したdict

        Returns:
            count(int): テスト結果を登録した人数
    """
    logger.info('Googleシート:定期試験登録・更新開始')
    count = 0
    for grade, data_list in result_dict.items():
        for data in data_list:
            regular = RegularExam.objects.filter(student_id=data['student_id'],
                                                 grade=data['grade'],
                                                 regular_id_id=data['regular_id']).first()
            student = Student.objects.get(id=data['student_id'])
            full_name = f'{student.last_name} {student.first_name}'
            if regular:
                regular.id = regular.id
                regular.student_id = data['student_id']
                regular.grade = data['grade']
                regular.exam_year = data['exam_year']
                regular.regular_id_id = data['regular_id']
                regular.english = data['english']
                regular.math = data['math']
                regular.japanese = data['japanese']
                regular.science = data['science']
                regular.social_studies = data['social_studies']
                regular.music = data['music']
                regular.art = data['art']
                regular.pe = data['pe']
                regular.tech = data['tech']
                regular.home = data['home']
                regular.sum_five = data['sum_five']
                regular.save()
                count += 1
                logger.info(f'Googleシート:定期試験[更新]１件({full_name})完了')

            else:
                new_regular = RegularExam(
                    student_id=data['student_id'],
                    grade=data['grade'],
                    exam_year=data['exam_year'],
                    regular_id_id=data['regular_id'],
                    english=data['english'],
                    math=data['math'],
                    japanese=data['japanese'],
                    science=data['science'],
                    social_studies=data['social_studies'],
                    music=data['music'],
                    art=data['art'],
                    pe=data['pe'],
                    tech=data['tech'],
                    home=data['home'],
                    sum_five=data['sum_five'],
                )
                new_regular.save()
                count += 1
                logger.info(f'Googleシート:定期試験[登録]１件({full_name})完了')
    logger.info('Googleシート:定期試験登録・更新終了')
    return count


def get_last_row(values, start_col):
    """get_last_row

        2次元配列の name の最終行番号を返す

        Args:
            values(list[list]): 結果の二次元配列
            start_col(int): 基準列

        Returns:
            row_num(int): 最終の配列の番号
    """
    for i, row in enumerate(values):
        try:
            if row[start_col + NAME_COL] != '':
                # 名前列に値があれば、その配列の番号をrow_numに代入して更新する
                row_num = i
        except Exception:
            pass
    return row_num


def is_registable(array, start_col):
    """is_registable

        2次元配列の name の最終行番号を返す

        Args:
            array(list): 配列
            start_col(int): 基準列

        Returns:
            bool: true → 指定の列の5科目がすべて'-'ではない(登録対象)
    """
    subject_num = 5
    five_sub_col = ENGLISH_COL
    for i in range(subject_num):
        if array[start_col + five_sub_col] != '-':
            return True
    return False

