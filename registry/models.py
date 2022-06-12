from decimal import Decimal
from decimal import ROUND_HALF_UP

from django.db import models


class RecordGroup(models.Model):
    id = models.IntegerField(primary_key=True)
    term_name = models.CharField(max_length=10)


class SchoolRecord(models.Model):
    student_id = models.IntegerField()
    grade = models.CharField(max_length=10)
    record_year = models.IntegerField()
    term_name = models.ForeignKey(RecordGroup, on_delete=models.SET_NULL, null=True)
    english = models.IntegerField(null=True)
    math = models.IntegerField(null=True)
    japanese = models.IntegerField(null=True)
    science = models.IntegerField(null=True)
    social_studies = models.IntegerField(null=True)
    music = models.IntegerField(null=True)
    art = models.IntegerField(null=True)
    pe = models.IntegerField(null=True)
    tech_home = models.IntegerField(null=True)
    sum_five = models.IntegerField(null=True)
    sum_all = models.IntegerField(null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['student_id', 'grade', 'record_year', 'term_name'],
                name='record_const'
            ),
        ]

    def to_list(self, subject_only=False):
        if subject_only:
            return [
                self.english,
                self.math,
                self.japanese,
                self.science,
                self.social_studies,
                self.music,
                self.art,
                self.pe,
                self.tech_home,
            ]
        else:
            return [
                self.student_id,
                self.grade,
                self.record_year,
                self.term_name,
                self.english,
                self.math,
                self.japanese,
                self.science,
                self.social_studies,
                self.sum_all,  # 面談シートを考慮して、ここに５科目合計を置く
                self.music,
                self.art,
                self.pe,
                self.tech_home,
                self.sum_all
            ]


class RegularExamGroup(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=10)


class RegularExam(models.Model):
    student_id = models.IntegerField()
    grade = models.CharField(max_length=10)
    exam_year = models.IntegerField()
    regular_id = models.ForeignKey(RegularExamGroup, on_delete=models.SET_NULL, null=True)
    english = models.CharField(max_length=5, null=True)
    math = models.CharField(max_length=5, null=True)
    japanese = models.CharField(max_length=5, null=True)
    science = models.CharField(max_length=5, null=True)
    social_studies = models.CharField(max_length=5, null=True)
    sum_five = models.CharField(max_length=5, null=True)
    music = models.CharField(max_length=5, null=True)
    art = models.CharField(max_length=5, null=True)
    pe = models.CharField(max_length=5, null=True)
    tech = models.CharField(max_length=5, null=True)
    home = models.CharField(max_length=5, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['student_id', 'grade', 'exam_year', 'regular_id'],
                name='regular_const'
            ),
        ]

    def to_list(self):
        return [
            self.student_id,
            self.grade,
            self.exam_year,
            self.regular_id,
            self.english,
            self.math,
            self.japanese,
            self.science,
            self.social_studies,
            self.sum_five,  # 面談シートを考慮して５科目合計はここに置く
            self.music,
            self.art,
            self.pe,
            self.tech,
            self.home
        ]


class PracticeMonth(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=10)


class PracticeExam(models.Model):
    student_id = models.IntegerField()
    grade = models.CharField(max_length=10)
    exam_year = models.IntegerField()
    month = models.ForeignKey(PracticeMonth, on_delete=models.SET_NULL, null=True)
    english_score = models.CharField(max_length=5, null=True)
    math_score = models.CharField(max_length=5, null=True)
    japanese_score = models.CharField(max_length=5, null=True)
    science_score = models.CharField(max_length=5, null=True)
    social_score = models.CharField(max_length=5, null=True)
    sum_three = models.CharField(max_length=5, null=True)
    sum_all = models.CharField(max_length=5, null=True)
    dev_three = models.CharField(max_length=5, null=True)
    dev_five = models.CharField(max_length=5, null=True)
    english_deviation = models.CharField(max_length=5, null=True)
    math_deviation = models.CharField(max_length=5, null=True)
    japanese_deviation = models.CharField(max_length=5, null=True)
    science_deviation = models.CharField(max_length=5, null=True)
    social_deviation = models.CharField(max_length=5, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['student_id', 'grade', 'exam_year', 'month'],
                name='practice_const'
            ),
        ]

    def to_list(self):
        return [
            self.student_id,
            self.grade,
            self.exam_year,
            self.month,
            self.english_score,
            self.math_score,
            self.japanese_score,
            self.science_score,
            self.social_score,
            self.sum_all,
            self.dev_three,
            self.dev_five
        ]

    def get_afbg(self, exam_record):
        A_score = exam_record.get_A_score()
        if not A_score == '':
            # 成績がある場合
            raw_B_score = Decimal(str(self.sum_all)) / Decimal('500') * Decimal('100')
            B_score = Decimal(str(raw_B_score)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
            return {
                'three_five': A_score * 3 + B_score * 5,
                'four_four': A_score * 4 + B_score * 4,
                'five_three': A_score * 5 + B_score * 3,
            }
        else:
            # 成績がない場合
            return {
                'three_five': '',
                'four_four': '',
                'five_three': '',
            }


class TimeLimit(models.Model):
    id = models.IntegerField(primary_key=True)
    sheet_name = models.CharField(max_length=10)
    limit_date = models.DateField()


class GradeIdLink(models.Model):
    id = models.IntegerField(primary_key=True)
    grade = models.CharField(max_length=10)
    start_id = models.IntegerField()
    birth_year = models.IntegerField()
