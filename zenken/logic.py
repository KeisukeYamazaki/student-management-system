import traceback
from collections import OrderedDict

from app_base import *
from zenken.models import Zenken

logger = getLogger(__name__)


def zenken_create_or_update(data):
    """zenken_create_or_update

        formで入力されたデータを受け取り、DBへ登録・更新する

        Args:
            data(dict): student_id, number, gender, city, term などの情報を含んだディクショナリー
                        キー：[リスト] の構成になっている
                        gender, city, term は登録の際に数字(文字列)に変換する必要あり

        Returns:
            True or False: 登録に成功すれば True, 途中で例外が発生したら False を返す
    """
    # dictのキーからlistを取得
    student_id_list = data['student_id']
    number_list = data['number']
    gender_list = data['gender']
    city_list = data['city']
    term_list = data['term']
    name_list = data['name']  # ログ出力用
    for i in range(len(student_id_list)):
        is_data = Zenken.objects.filter(student_id=student_id_list[i]).first()
        try:
            if not is_data:
                new_zenken = Zenken(
                    student_id=int(student_id_list[i]),
                    zenken_number=number_list[i],
                    gender=convert_gender(gender_list[i]),
                    enrollment='1',
                    prefecture='14',
                    city=convert_city(city_list[i]),
                    recordTerm=convert_term(term_list[i]),
                )
                new_zenken.save()
                logger.info(f'{i + 1}/{len(student_id_list)} 件目: {name_list[i]} 全県模試データ[新規登録]')
            else:
                zenken = Zenken.objects.get(student_id=student_id_list[i])
                zenken.student_id = int(student_id_list[i])
                zenken.zenken_number = number_list[i]
                zenken.gender = gender_list[i]
                zenken.enrollment = '1'
                zenken.prefecture = '14'
                zenken.city = city_list[i]
                zenken.recordTerm = term_list[i]
                zenken.save()
                logger.info(f'{i + 1}/{len(student_id_list)} 件目: {name_list[i]} 全県模試データ[更新]')
        except:
            logger.error(f'{i + 1}/{len(student_id_list)} 件目: {name_list[i]} 登録失敗')
            traceback.print_exc()
            return False

    return True


def convert_gender(gender):
    if gender in ['1', '2']:
        return '男' if gender == '1' else '女'
    if gender in ['男', '女']:
        return '1' if gender == '男' else '2'


def convert_city(city):
    city_dict = cities()
    number_list = [n for n in city_dict.keys()]
    city_list = [c for c in city_dict.values()]
    # 番号が渡ってきたら市区町村名を返却し、
    if city in number_list:
        for i in range(len(number_list)):
            if city == number_list[i]:
                return city_list[i]
    # 市区町村名が渡ってきたら番号を返す
    if city in city_list:
        for i in range(len(city_list)):
            if city == city_list[i]:
                return number_list[i]


def convert_term(term):
    if term in ['1', '2']:
        return '３学期制' if term == '1' else '２学期制'
    if term in ['３学期制', '２学期制']:
        return '1' if term == '３学期制' else '2'


# 今後全県模試に登録する市区町村が増えた場合は、ここだけを変更する
def cities():
    city_dict = OrderedDict()
    city_dict['114'] = '瀬谷区'
    city_dict['112'] = '旭区'
    city_dict['116'] = '泉区'
    city_dict['213'] = '大和市'
    return city_dict
