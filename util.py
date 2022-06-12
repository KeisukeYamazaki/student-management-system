import datetime

import pykakasi


def convert_grade(grade_value):
    """convert_grade

        日本語の学年(中３など)をアルファベットと数字の学年(j3など)と相互に変換する

        Args:
            grade_value(str): 日本語表記の学年 or アルファベット + 数字 表記の学年

        Returns:
            変換した学年
    """
    grade_list = ['中３', '中２', '中１', '小６', '小５', '小４', '小３']
    grade_values = ['j3', 'j2', 'j1', 'e6', 'e5', 'e4', 'e3']
    if grade_value in grade_values:
        # j3 -> 中３
        for i in range(len(grade_values)):
            if grade_value == grade_values[i]:
                return grade_list[i]
    else:
        # 中３ -> j3
        for i in range(len(grade_list)):
            if grade_value == grade_list[i]:
                return grade_values[i]


def get_school_year():
    """get_school_year

        年度を取得する

        Returns:
            school_year: 年度
    """
    today = datetime.date.today()
    if 1 <= today.month <= 3:
        return today.year - 1
    else:
        return today.year


def katakana_to_romaji(katakana):
    kakasi = pykakasi.kakasi()
    text = katakana
    kakasi.setMode("K", "a")  # Katakana to ascii
    converter = kakasi.getConverter()
    return converter.do(text)


def str_for_int_check(word):
    try:
        int(word)
    except ValueError:
        return False
    return True


def str_for_float_check(word):
    try:
        float(word)
    except ValueError:
        return False
    return True


def expireEncoda(object):
    if isinstance(object, datetime.date):
        return object.isoformat()


def convert_school(school):
    """school_convert

        日本語の校舎名(橋戸校など)とアルファベットの校舎名(hashidoなど)を相互に変換する

        Args:
            school(str): 日本語表記の校舎 or アルファベット表記の校舎

        Returns:
            変換した校舎
    """
    kanji_list = ['橋戸校', '瀬谷校', '大和校', '本校']
    romaji_list = ['hashido', 'seya', 'yamato', 'honko']
    if school in kanji_list:
        for i in range(len(kanji_list)):
            if school == kanji_list[i]:
                return romaji_list[i]
    if school in romaji_list:
        for i in range(len(romaji_list)):
            if school == romaji_list[i]:
                return kanji_list[i]
