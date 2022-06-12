from decimal import Decimal
from decimal import ROUND_HALF_UP


def exam_ratio_calc(score, public_high_school, exam_record):
    """exam_ratio_calc

        (af + bg)値、またはS値をもとに、入試に必要な点数を算出する

        Args:
            score(Decimal): (af + bg)値、またはS値
            public_high_school (PublicHighSchool): PublicHighSchoolのインスタンス
            exam_record(ExamRecord, optional): ExamRecordのインスタンス

        Returns:
            score(float): 入試に必要な点数 or ボーダー点数
    """
    ratio = public_high_school.score_ratio
    if '※' in ratio:
        ratio = ratio.replace('※', '').strip()
    ratio_list = ratio.split(':')

    f = int(ratio_list[0])  # 内申の比率
    g = int(ratio_list[1])  # 学力検査の比率
    h = int(ratio_list[2])  # 面接の比率
    if len(ratio_list) == 4:
        special_ratio = int(ratio_list[3])

    a = (exam_record.one_three_five / 135) * 100  # a: 内申を100点満点に換算したもの
    bg = score - Decimal(str(a * f))  # b: 学力検査の点数を100点満点に換算したもの
    return Decimal(str(500 * (bg / g) / 100)).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)

