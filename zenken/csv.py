import csv
import tempfile

from app_base import *
from registry.models import SchoolRecord
from student.models import Student
from util import convert_school
from zenken.models import Zenken

logger = logger = getLogger(__name__)


def make_csv(school, grade, students):
    # 最終的に出力する全ての行を入れる2次元配列
    all_lines = []

    # １行目のデータを入れる配列
    first_line = []

    # 1行目-1: 学年
    if grade == '中３':
        first_line.append(23)
    elif grade == '中２':
        first_line.append(22)
    elif grade == '中１':
        first_line.append(21)

    # 1行目-2 団体コード
    first_line.append(128)

    # 1行-3 校舎番号(本校の処理が必要になる)
    if school == '橋戸校':
        first_line.append(1)
    elif school == '瀬谷校':
        first_line.append(2)
    elif school == '大和校':
        first_line.append(3)

    # 1行目-4
    # 中２の11月~3月は 2a ではなく 2b になる
    is_Nov_to_Mar = today.month <= 3 or 11 <= today.month
    if grade == '中２' and is_Nov_to_Mar:
        first_line.append('2b')
    else:
        first_line.append('2a')

    # すべての行に1行目を追加する
    all_lines.append(first_line)

    # 2行目以降は1人1人の生徒のデータ(生徒の人数ループする)
    # 模試番号順にソートするので、ソート用の配列を作ってこれに格納していく
    not_sort_list = []
    for student in students:
        line = []
        # 全県オブジェクトを生徒番号から取得
        zenken = Zenken.objects.filter(student_id=student.id).first()
        if not zenken:
            # データがない場合はログに出力して飛ばす
            logger.warning(f'全県模試CSV出力 データなし：{student.last_name} {student.first_name}')
            continue
        # 2行目以降-1 模試番号
        line.append(zenken.zenken_number)

        # 2行目以降-2 性別
        line.append(zenken.gender)

        # 2行目以降-3 区分
        line.append(zenken.enrollment)

        # 2行目以降-4 名前(タブルクォーテーションで囲み、姓名の間は全角スペース)
        line.append(f'"{student.last_name}　{student.first_name}"')

        # 2行目以降-5 フリガナ(タブルクォーテーションで囲み、姓名の間は全角スペース)
        line.append(f'"{student.last_ruby}　{student.first_ruby}"')

        # 2行目以降-6 都道府県名
        line.append(zenken.prefecture)

        # 2行目以降-7 市区町村
        line.append(zenken.city)

        # 2行目以降-8 各学期の成績
        line = add_record(student, line)

        # このあとソートする配列に格納する
        not_sort_list.append(line)

    # 2行目以降をソートする
    sorted_list = sorted(not_sort_list, key=lambda x: int(x[0]))
    # ソートされたものを1行つづ加えていく
    for line in sorted_list:
        all_lines.append(line)
    # 作成するファイルの名前を設定
    romaji_school = convert_school(school)
    file_name = f'{today.strftime("%Y%m%d")}{romaji_school}.csv'

    # csvファイルを作成する
    with open(file_name, 'w') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_NONE, escapechar=' ')
        writer.writerows(all_lines)
    # 強引なやりかただが、上記のままだと不要な半角スペースができてしまうので、それを消す
    with open(file_name, 'r') as f2:
        # 作ったファイルを読み込み、半角スペースを消す
        file_data = f2.read().replace(' ', '')
    # 上書きする
    with open(file_name, 'w') as f3:
        f3.write(file_data)

    # 作成したファイル名を返す
    return file_name


def add_record(student, line):
    """add_record

        引数で受けた全県模試の登録に必要な配列に、登録されている成績を加えて返す

        Args:
            student(Student): Studentインスタンス
            line(list): あらかじめ模試番号, 性別, 区分, 名前, フリガナ, 都道府県, 市町村の情報が入った配列

        Returns:
            引数で受けた配列に登録されている成績を加えたもの

    """
    # get_term_listに渡す grade と term を設定
    grade = student.grade
    term = Zenken.objects.get(student_id=student.id).recordTerm
    # 学年と学期を渡して、取得する必要がある成績の学年と学期が入ったリストを受ける
    terms = get_term_list(grade, term)
    for i in range(len(terms)):
        record = SchoolRecord.objects.filter(student_id=student.id,
                                             grade=terms[i][0],
                                             term_name_id=terms[i][1])
        # 成績があればそれをリストに追加し、成績がない場合は空文字10コをリストに入れる
        if record:
            line.append(term)
            # 9科目の成績が順に入ったリストを取得
            subjects = record.to_list(subject_only=True)
            for subject in subjects:
                line.append(subject)
        else:
            for _ in range(10):
                line.append('')
    return line


def get_term_list(grade, term, is_Nov_to_Mar=False):
    """get_term_list

        学年と学期を引数で受け、取得する必要がある成績の「学年」と「学期」のを入れた2次元配列を返す

        Args:
            grade(str): 学年('中３', '中２', '中１' のいずれか)
            term(str): 学期(1:１学期, 2:前期, 3:２学期, 4: 後期, 5: ３学期)
            is_Nov_to_Mar(bool): 11月〜３月かどうかの判定。中２の成績取得で使う。

        Returns:
            取得する必要がある成績の「学年」と「学期」のを入れた2次元配列

        Note:
            ２学期制の場合、登録する必要がない部分は['', 0]として、成績を取得する際にNoneを受けるようにする
    """
    if grade == '中３':
        if term == '1':
            return [['中２', 5], ['中３', 1], ['中３', 3]]
        if term == '2':
            return [['中２', 4], ['中３', 2], ['中３', 4]]
    if grade == '中２':
        if term == '1':
            if not is_Nov_to_Mar:
                return [['中１', 5], ['中２', 1], ['中２', 3]]
            else:
                return [['中２', 1], ['中２', 3], ['中２', 5]]
        if term == '2':
            if not is_Nov_to_Mar:
                return [['中１', 4], ['', 0], ['中２', 2]]
            else:
                return [['', 0], ['中２', 2], ['中２', 4]]
    if grade == '中１':
        if term == '1':
            return [['中１', 1], ['中１', 3], ['中１', 5]]
        if term == '2':
            return [['', 0], ['中１', 2], ['中１', 4]]