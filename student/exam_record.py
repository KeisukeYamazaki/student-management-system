from decimal import Decimal
from decimal import ROUND_HALF_UP

from registry.models import SchoolRecord


class ExamRecord:
    four_five = None
    one_three_five = None
    two_five = None
    five_zero = None
    seven_five = None
    one_five = None
    three_zero = None

    def __init__(self, student):
        school_records = {}
        latest_record = None

        for i in range(3):
            if i == 0:
                g = '中１'
            elif i == 1:
                g = '中２'
            else:
                g = '中３'
            school_records[g] = SchoolRecord.objects.filter(student_id=student.id, grade=g).order_by('id')
            # 最新の成績を取得
            for record in school_records[g]:
                if record:
                    latest_record = record

        if not latest_record:
            # 成績が１つもない場合は、すべて''にして終了する
            self.four_five = ''
            self.one_three_five = ''
            self.two_five = ''
            self.five_zero = ''
            self.seven_five = ''
            self.one_five = ''
            self.three_zero = ''
            return

        if student.grade == '中３' and school_records['中２']:
            term_name_list = []
            # 登録されている中２の成績の学期名をリストに格納
            for record in school_records['中２']:
                term_name = record.term_name.term_name
                term_name_list.append(term_name)
            # 中２の３学期または後期の成績があるか
            if ('３学期' in term_name_list) or ('後期' in term_name_list):
                # 中２の成績から ３学期 または 後期 の成績を見つける
                for record in school_records['中２']:
                    term_name = record.term_name.term_name
                    if term_name == '３学期' or term_name == '後期':
                        second_grade_record = record

                self.four_five = latest_record.sum_all
                self.one_three_five = latest_record.sum_all * 2 + second_grade_record.sum_all
                self.two_five = latest_record.sum_five
                self.five_zero = latest_record.sum_five + second_grade_record.sum_five
                self.seven_five = latest_record.sum_five * 2 + second_grade_record.sum_five
                self.one_five = sum([latest_record.english, latest_record.math, latest_record.japanese])
                second_grade_record_three_sub = sum([
                    second_grade_record.english,
                    second_grade_record.math,
                    second_grade_record.japanese
                ])
                self.three_zero = self.one_five + second_grade_record_three_sub

        if not self.four_five:
            self.four_five = latest_record.sum_all
            self.one_three_five = latest_record.sum_all * 3
            self.two_five = latest_record.sum_five
            self.five_zero = latest_record.sum_five * 2
            self.seven_five = latest_record.sum_five * 3
            self.one_five = sum([latest_record.english, latest_record.math, latest_record.japanese])
            self.three_zero = self.one_five * 2

    def get_A_score(self):
        if not self.one_three_five == '':
            A_score = Decimal(str(self.one_three_five)) / Decimal('135') * Decimal('100')
            return Decimal(str(A_score)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
        else:
            # 成績がない場合
            return ''

