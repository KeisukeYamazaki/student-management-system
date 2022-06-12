import traceback

from app_base import *
from student.models import Student, PublicHighSchool
from student.models import FuturePath
from util import get_school_year
from registry.models import SchoolRecord
from registry.models import RegularExam
from registry.models import PracticeExam

logger = getLogger(__name__)


def school_record_create_or_update(registry_data, personal=False):

    if personal:
        counter = len(registry_data['grade'])
        logger.info('個人成績登録開始')
    else:
        counter = len(registry_data['last_name'])
        logger.info('学年成績登録開始')
    for i in range(counter):
        if not registry_data['id'][i] == '':
            record = SchoolRecord.objects.get(id=int(registry_data['id'][i]))
            if personal:
                record.student_id = int(registry_data['student_id'][0])
            else:
                record.student_id = int(registry_data['student_id'][i])
            record.grade = registry_data['grade'][i]
            record.record_year = int(registry_data['record_year'][i])
            record.term_name_id = int(registry_data['term_name'][i])
            record.english = int(registry_data['english'][i])
            record.math = int(registry_data['math'][i])
            record.japanese = int(registry_data['japanese'][i])
            record.science = int(registry_data['science'][i])
            record.social_studies = int(registry_data['social_studies'][i])
            record.music = int(registry_data['music'][i])
            record.art = int(registry_data['art'][i])
            record.pe = int(registry_data['pe'][i])
            record.tech_home = int(registry_data['tech_home'][i])
            record.sum_five = int(registry_data['sum_five'][i])
            record.sum_all = int(registry_data['sum_all'][i])
            record.save()
            logger.info('成績[更新]１件完了')

        elif registry_data['id'][i] == '' and not registry_data['english'][i] == '':
            # id は '' だが、英語には値が入っている場合、新規登録処理として扱う
            student_id = registry_data['student_id'][0] if personal else registry_data['student_id'][i]
            new_record = SchoolRecord(
                student_id=int(student_id),
                grade=registry_data['grade'][i],
                record_year=int(registry_data['record_year'][i]),
                term_name_id=int(registry_data['term_name'][i]),
                english=int(registry_data['english'][i]),
                math=int(registry_data['math'][i]),
                japanese=int(registry_data['japanese'][i]),
                science=int(registry_data['science'][i]),
                social_studies=int(registry_data['social_studies'][i]),
                music=int(registry_data['music'][i]),
                art=int(registry_data['art'][i]),
                pe=int(registry_data['pe'][i]),
                tech_home=int(registry_data['tech_home'][i]),
                sum_five=int(registry_data['sum_five'][i]),
                sum_all=int(registry_data['sum_all'][i]),
            )
            new_record.save()
            logger.info('成績[登録]１件完了')


def regular_exam_create_or_update(registry_data, personal=False):

    if personal:
        counter = len(registry_data['grade'])
        logger.info('個人定期試験登録開始')
    else:
        counter = len(registry_data['last_name'])
        logger.info('一括定期試験登録開始')
    for i in range(counter):
        if not registry_data['id'][i] == '':
            regular = RegularExam.objects.get(id=int(registry_data['id'][i]))
            if personal:
                regular.student_id = int(registry_data['student_id'][0])
            else:
                regular.student_id = int(registry_data['student_id'][i])
            regular.grade = registry_data['grade'][i]
            regular.exam_year = int(registry_data['exam_year'][i])
            regular.regular_id_id = int(registry_data['regular_id'][i])
            regular.english = registry_data['english'][i]
            regular.math = registry_data['math'][i]
            regular.japanese = registry_data['japanese'][i]
            regular.science = registry_data['science'][i]
            regular.social_studies = registry_data['social_studies'][i]
            regular.music = registry_data['music'][i]
            regular.art = registry_data['art'][i]
            regular.pe = registry_data['pe'][i]
            regular.tech = registry_data['tech'][i]
            regular.home = registry_data['home'][i]
            regular.sum_five = registry_data['sum_five'][i]
            regular.save()
            logger.info('定期試験[更新]１件完了')

        elif registry_data['id'][i] == '' and not registry_data['regular_id'][i] == '':
            # id は '' だが、時期が '' ではない場合、新規登録処理を行う
            student_id = registry_data['student_id'][0] if personal else registry_data['student_id'][i]
            new_regular = RegularExam(
                student_id=int(student_id),
                grade=registry_data['grade'][i],
                exam_year=int(registry_data['exam_year'][i]),
                regular_id_id=int(registry_data['regular_id'][i]),
                english=registry_data['english'][i],
                math=registry_data['math'][i],
                japanese=registry_data['japanese'][i],
                science=registry_data['science'][i],
                social_studies=registry_data['social_studies'][i],
                music=registry_data['music'][i],
                art=registry_data['art'][i],
                pe=registry_data['pe'][i],
                tech=registry_data['tech'][i],
                home=registry_data['home'][i],
                sum_five=registry_data['sum_five'][i],
            )
            new_regular.save()
            logger.info('定期試験[登録]１件完了')


def practice_exam_create_or_update(registry_data):

    counter = len(registry_data['grade'])
    logger.info('個人模試登録開始')

    for i in range(counter):
        if not registry_data['id'][i] == '':
            practice = PracticeExam.objects.get(id=int(registry_data['id'][i]))
            practice.student_id = int(registry_data['student_id'][0])
            practice.grade = registry_data['grade'][i]
            practice.exam_year = int(registry_data['exam_year'][i])
            practice.month_id = int(registry_data['month_id'][i])
            practice.english_score = registry_data['english'][i]
            practice.math_score = registry_data['math'][i]
            practice.japanese_score = registry_data['japanese'][i]
            practice.science_score = registry_data['science'][i]
            practice.social_score = registry_data['social_studies'][i]
            practice.sum_three = registry_data['sum_three'][i]
            practice.sum_all = registry_data['sum_all'][i]
            practice.dev_three = registry_data['dev_three'][i]
            practice.dev_five = registry_data['dev_five'][i]
            practice.english_deviation = registry_data['english_deviation'][i]
            practice.math_deviation = registry_data['math_deviation'][i]
            practice.japanese_deviation = registry_data['japanese_deviation'][i]
            practice.science_deviation = registry_data['science_deviation'][i]
            practice.social_deviation = registry_data['social_deviation'][i]
            practice.save()
            logger.info('模試[更新]１件完了')

        elif registry_data['id'][i] == '' and not registry_data['month_id'][i] == '':
            # id は '' だが、時期が '' ではない場合、新規登録処理を行う
            new_practice = PracticeExam(
                student_id=int(registry_data['student_id'][0]),
                grade=registry_data['grade'][i],
                exam_year=int(registry_data['exam_year'][i]),
                month_id=int(registry_data['month_id'][i]),
                english_score=registry_data['english'][i],
                math_score=registry_data['math'][i],
                japanese_score=registry_data['japanese'][i],
                science_score=registry_data['science'][i],
                social_score=registry_data['social_studies'][i],
                sum_three=registry_data['sum_three'][i],
                sum_all=registry_data['sum_all'][i],
                dev_three=registry_data['dev_three'][i],
                dev_five=registry_data['dev_five'][i],
                english_deviation=registry_data['english_deviation'][i],
                math_deviation=registry_data['math_deviation'][i],
                japanese_deviation=registry_data['japanese_deviation'][i],
                science_deviation=registry_data['science_deviation'][i],
                social_deviation=registry_data['social_deviation'][i],
            )
            new_practice.save()
            logger.info('模試[登録]１件完了')


def get_record_school_year(now_grade, select_grade):
    """get_record_school_year

        成績登録の年度を取得する

        Args:
            now_grade(str): 現在の学年
            select_grade(str): 選択された学年

        Returns:
            year(int): 年度
    """
    this_month = datetime.date.today().month

    # 現在の年度を取得
    year = get_school_year()

    # 中３の場合
    if now_grade == 'j3':
        # 選択された学年に応じて現在の年度 -1, -2を行う
        if select_grade == 'j2':
            year = get_school_year() - 1
        elif select_grade == 'j1':
            year = get_school_year() - 2
    # 中２の場合
    elif now_grade == 'j2':
        # 選択された学年に応じて現在の年度 -1を行う
        if select_grade == 'j1':
            year = get_school_year() - 1

    # 今月が１〜３月 かつ 現在の学年と選択された学年が等しくない 場合
    # = １月〜３月に「現中２の中１時」「現中３の中２・中１時」の成績を入力する場合
    if this_month < 4 and not now_grade == select_grade:
        year += 1

    return year


def student_name_to_id(students, student_name):
    """student_name_to_id

        生徒名からidを取得する

        Args:
            students(QueryDict): 当該学年などの生徒のQueryDict
            student_name (str): idを取得する生徒の名前

        Returns:
            id(str): 生徒のid
    """
    similar_str_list = [['高', '髙'], ['崎', '﨑'], ['国', '國']]
    student_name = student_name.replace(' ', '')
    for student in students:
        full_name = student.last_name + student.first_name
        if student_name == full_name:
            return student.id
        # 類似の漢字はループを回して探す
        for similar_str in similar_str_list:
            if student_name == full_name.replace(similar_str[0], similar_str[1]):
                return student.id
            if student_name == full_name.replace(similar_str[1], similar_str[0]):
                return student.id


def high_school_name_to_id(high_schools, high_school_name):
    """high_school_name_to_id

        高校からidを取得する

        Args:
            high_schools(QueryDict): 公立高校すべてのQueryDict
            high_school_name (str): idを取得する高校の名前

        Returns:
            id(str): 高校のid
    """
    for high_school in high_schools:
        if high_school_name == high_school.name:
            return high_school.id
        return 0


def register_from_zenken(practice_data, grade, exam_year, month):
    """register_from_zenken

        全県模試データからPractice_examとFuture_pathを登録する

        Args:
            practice_data(list): 生徒の模試データ(dict)を含んだリスト
            grade(str): 登録するデータの学年。'中３', '中２', '中１' のいずれか
            exam_year(int): 模試実施年度
            month(str): 月の名前の数字(7, 8, 10, 12, 1, 3 いずれか)

        Returns:
            True or False: 登録に成功すれば True, 途中で例外が発生したら False を返す
    """
    students = Student.objects.filter(grade=grade)
    high_schools = PublicHighSchool.objects.all()
    not_registered_list = []
    # ３月の場合は、登録のためにここで学年を１つさげる
    if month == '3':
        if grade == '中３':
            grade = '中２'
        elif grade == '中２':
            grade = '中１'
    # 模試の受験年度は、登録するのが４月なら前年度とする
    # 月を月のidに変換
    if month == '7':
        month_id = 1
    elif month == '8':
        month_id = 2
    elif month == '10':
        month_id = 3
    elif month == '12':
        month_id = 4
    elif month == '1':
        month_id = 5
    elif month == '3':
        month_id = 6
    for data in practice_data:
        student_id = student_name_to_id(students, data['name'])
        # IDが返ってこなかった場合(=生徒が登録されていない場合)、
        # 登録できなかった生徒のリストに入れて、ループを飛ばす
        if student_id is None:
            not_registered_list.append(data['name'])
            continue
        practice_exam = PracticeExam.objects.filter(student_id=student_id,
                                                    grade=grade,
                                                    exam_year=exam_year,
                                                    month_id=month_id).exists()
        # Practice_examの登録
        try:
            # 新しいレコードとして登録する場合
            if not practice_exam:
                new_practice_exam = PracticeExam(
                    student_id=student_id,
                    grade=grade,
                    exam_year=exam_year,
                    month_id=month_id,
                    english_score=data['english_score'],
                    math_score=data['math_score'],
                    japanese_score=data['japanese_score'],
                    science_score=data['science_score'],
                    social_score=data['social_score'],
                    sum_three=data['sum_three'],
                    sum_all=data['sum_all'],
                    dev_three=data['dev_three'],
                    dev_five=data['dev_all'],
                    english_deviation=data['english_deviation'],
                    math_deviation=data['math_deviation'],
                    japanese_deviation=data['japanese_deviation'],
                    science_deviation=data['science_deviation'],
                    social_deviation=data['social_deviation'],
                )
                new_practice_exam.save()
                logger.info('模試[登録]１件完了: ' + data['name'])
            # 更新処理として登録する場合
            else:
                practice_exam = PracticeExam.objects.get(student_id=student_id,
                                                         grade=grade,
                                                         exam_year=exam_year,
                                                         month_id=month_id)
                practice_exam.student_id = student_id
                practice_exam.grade = grade
                practice_exam.exam_year = exam_year
                practice_exam.month_id = month_id
                practice_exam.english_score = data['english_score']
                practice_exam.math_score = data['math_score']
                practice_exam.japanese_score = data['japanese_score']
                practice_exam.science_score = data['science_score']
                practice_exam.social_score = data['social_score']
                practice_exam.sum_three = data['sum_three']
                practice_exam.sum_all = data['sum_all']
                practice_exam.dev_three = data['dev_three']
                practice_exam.dev_five = data['dev_all']
                practice_exam.english_deviation = data['english_deviation']
                practice_exam.math_deviation = data['math_deviation']
                practice_exam.japanese_deviation = data['japanese_deviation']
                practice_exam.science_deviation = data['science_deviation']
                practice_exam.social_deviation = data['social_deviation']
                practice_exam.save()
                logger.info('模試[更新]１件完了: ' + data['name'])
        # KeyError(=名前はあるが、試験のデータが欠けている)場合は、登録できなかったリストに入れて、continue
        except KeyError:
            not_registered_list.append(data['name'])
            continue
        # それ以外の例外は処理を留める
        except:
            traceback.print_exc()
            return False,

        # FuturePathの登録
        # future_path = FuturePath.objects.filter(student_id=student_id).exists()
        # try:
        #     if future_path:
        #         future_path = FuturePath.objects.get(student_id=student_id)
        #         future_path.first_choice_id = high_school_name_to_id(high_schools, data['first_choice'])
        #         future_path.second_choice_id = high_school_name_to_id(high_schools, data['second_choice'])
        #         future_path.third_choice_id = high_school_name_to_id(high_schools, data['third_choice'])
        #         future_path.record_date = datetime.date.today()
        #         future_path.save()
        #         logger.info('進路情報[更新]１件完了: ' + data['name'])
        #     else:
        #         new_future_path = FuturePath(
        #             student_id=student_id,
        #             first_choice_id=high_school_name_to_id(high_schools, data['first_choice']),
        #             second_choice_id=high_school_name_to_id(high_schools, data['second_choice']),
        #             third_choice_id=high_school_name_to_id(high_schools, data['third_choice']),
        #             record_date=datetime.date.today(),
        #         )
        #         new_future_path.save()
        #         logger.info('進路情報[新規登録]１件完了: ' + data['name'])
        # except:
        #     traceback.print_exc()
        #     return False,

    return True, not_registered_list
