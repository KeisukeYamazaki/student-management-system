import datetime
import math
from decimal import Decimal
from decimal import ROUND_HALF_UP
from statistics import mean

from django.db import models

from student.exam_ratio_calc import exam_ratio_calc
from util import str_for_float_check


class ElementarySchool(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)


class JuniorHighSchool(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    term = models.CharField(max_length=20, null=True)


class HomeRoom(models.Model):
    name = models.CharField(max_length=10, primary_key=True)
    grade = models.CharField(max_length=10)


class Student(models.Model):
    id = models.IntegerField(primary_key=True)
    last_name = models.CharField(max_length=10)
    first_name = models.CharField(max_length=10)
    last_ruby = models.CharField(max_length=10)
    first_ruby = models.CharField(max_length=10)
    grade = models.CharField(max_length=10)
    school = models.CharField(max_length=10)
    home_room = models.CharField(max_length=10, null=True)
    local_school = models.CharField(max_length=10, null=True)
    entry_grade = models.CharField(max_length=10, null=True)
    birthday = models.DateField(null=True)
    club = models.CharField(max_length=50, null=True)
    parents = models.CharField(max_length=50, null=True)
    siblings = models.CharField(max_length=50, null=True)
    info = models.TextField(max_length=1000, null=True)

    def to_string(self):
        return {
            'lastname': self.last_name,
            'firstname': self.first_name,
            'grade': self.grade,
            'home_room': self.home_room
        }


class PrivateHighSchool(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    course = models.CharField(max_length=20, null=True)
    exam_way = models.CharField(max_length=20, null=True)
    document_selection = models.NullBooleanField()
    boys_or_girls_only = models.CharField(max_length=5, null=True)
    standard_score = models.CharField(max_length=100, null=True)
    score_percentage = models.IntegerField(null=True)
    features = models.CharField(max_length=100, null=True)
    commuting_time = models.IntegerField(null=True)
    using_bus = models.NullBooleanField()
    remarks = models.CharField(max_length=100, null=True)
    access = models.CharField(max_length=75, null=True)
    update_date = models.DateField(null=True)

    def to_list(self):
        return [
            self.name,
            self.course,
            self.standard_score,
            self.access
        ]


class PublicHighSchool(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    score_ratio = models.CharField(max_length=10, null=True)
    school_record_this_year = models.CharField(max_length=10, null=True)
    school_record_last_year = models.CharField(max_length=10, null=True)
    school_record_three_years_ago = models.CharField(max_length=10, null=True)
    exam_score_this_year = models.CharField(max_length=10, null=True)
    exam_score_last_year = models.CharField(max_length=10, null=True)
    exam_score_three_years_ago = models.CharField(max_length=10, null=True)
    s_score_this_year = models.CharField(max_length=10, null=True)
    s_score_last_year = models.CharField(max_length=10, null=True)
    s_score_three_years_ago = models.CharField(max_length=10, null=True)
    border_this_year = models.CharField(max_length=10, null=True)
    border_last_year = models.CharField(max_length=10, null=True)
    border_three_years_ago = models.CharField(max_length=10, null=True)
    second_border_this_year = models.CharField(max_length=10, null=True)
    second_border_last_year = models.CharField(max_length=10, null=True)
    second_border_three_years_ago = models.CharField(max_length=10, null=True)
    competition_rate_this_year = models.CharField(max_length=10, null=True)
    competition_rate_last_year = models.CharField(max_length=10, null=True)
    competition_rate_three_years_ago = models.CharField(max_length=10, null=True)
    extra1 = models.ForeignKey(PrivateHighSchool, on_delete=models.SET_NULL, null=True, related_name='extra1')
    extra2 = models.ForeignKey(PrivateHighSchool, on_delete=models.SET_NULL, null=True, related_name='extra2')
    extra3 = models.ForeignKey(PrivateHighSchool, on_delete=models.SET_NULL, null=True, related_name='extra3')
    extra4 = models.ForeignKey(PrivateHighSchool, on_delete=models.SET_NULL, null=True, related_name='extra4')
    extra5 = models.ForeignKey(PrivateHighSchool, on_delete=models.SET_NULL, null=True, related_name='extra5')
    access = models.CharField(max_length=75, null=True)

    def to_string(self):
        return {
            'id': self.id,
            'name': self.name,
            'score_ratio': self.score_ratio,

        }

    def get_data(self, kind, exam_record=''):
        """get_data_

        合格者平均内申, 合格者平均入試点数, 合格者ボーダー点数のいずれかの過去３年平均と直近の数値を返す
        (exam_record)がある場合：
            exam_recordの数値から計算した、合格者平均内申, 合格者平均入試点数, 合格者ボーダー点数のいずれか
            の必要数値を返す

        Args:
            self (PublicHighSchool): PublicHighSchoolのインスタンス
            kind (str): school_record, exam_score, border のいずれかの種類
            exam_record(ExamRecord, optional): ExamRecordのインスタンス

        Returns:
           data_dict : key 'average(3年間の平均)' or 'late(直近)', value: average, late それぞれの値
        """
        data_dict = {}
        records = []
        if self.id == 0:
            # 志望校がない(=0)の場合はそれぞれ''を返す
            data_dict['late'] = ''
            data_dict['average'] = ''
            return data_dict
        # school_record, exam_score, border の種類によって分岐し、それぞれの３年分の値のリストを作る
        if kind == 'school_record':
            data = [self.school_record_three_years_ago, self.school_record_last_year, self.school_record_this_year]
        elif kind == 'exam_score':
            if exam_record:
                data = [self.s_score_three_years_ago, self.s_score_last_year, self.s_score_this_year]
            else:
                data = [self.exam_score_three_years_ago, self.exam_score_last_year, self.exam_score_this_year]
        elif kind == 'border':
            data = [self.border_three_years_ago, self.border_last_year, self.border_this_year]
        for value in data:
            if str_for_float_check(value):
                # floatに変換できる(正常な値がある)場合はリストに入れ、かつ data_dict['late'] の値を更新
                records.append(float(value))
                data_dict['late'] = Decimal(str(value))
        if not len(records) == 0:
            data_dict['average'] = Decimal(str(mean(records))).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)
        else:
            # 何もデータが無かった場合(=高校名は存在しているが、中身の数値がない場合)はそれぞれ''を返す
            data_dict['late'] = ''
            data_dict['average'] = ''
            return data_dict

        # 以下、exam_record がある場合の処理
        if exam_record and kind == 'school_record':
            if not exam_record.four_five == '':
                # 平均に達するのに必要な内申 = (/135の内申 - 合格者平均内申)2
                need_late_record = math.ceil((exam_record.one_three_five - data_dict['late']) / 2)
                if need_late_record > 0:
                    data_dict['late'] = '+' + str(need_late_record)
                else:
                    data_dict['late'] = need_late_record
                need_average_record = math.ceil((exam_record.one_three_five - data_dict['average']) / 2)
                if need_average_record > 0:
                    data_dict['average'] = '+' + str(need_average_record)
                else:
                    data_dict['average'] = need_average_record
        elif exam_record and (kind == 'exam_score' or kind == 'border'):
            if not exam_record.four_five == '':
                data_dict['late'] = exam_ratio_calc(data_dict['late'], self, exam_record)
                data_dict['average'] = exam_ratio_calc(data_dict['average'], self, exam_record)
        return data_dict

    def get_data_all_kind(self, exam_record=''):
        """get_data_all_kind

        合格者平均内申, 合格者平均入試点数, 合格者ボーダー点数の過去３年平均と直近の数値を返す

        Args:
            self (PublicHighSchool): PublicHighSchoolのインスタンス
            exam_record(ExamRecord, optional): ExamRecordのインスタンス

        Returns:
           score_dict : key 'ave(3年間の平均)' or 'late(直近)',
                        value(dict): record: 平均内申, score: 平均入試点数, border: ボーダー点数
        """
        score_dict = {'ave': {}, 'late': {}}
        kinds = ['school_record', 'exam_score', 'border']
        for kind in kinds:
            if exam_record:
                score_dict['ave'][kind] = self.get_data(kind, exam_record)['average']
                score_dict['late'][kind] = self.get_data(kind, exam_record)['late']
            else:
                score_dict['ave'][kind] = self.get_data(kind)['average']
                score_dict['late'][kind] = self.get_data(kind)['late']
        return score_dict

    def to_list(self):
        return [
            self.name,
            self.score_ratio,
            self.school_record_this_year,
            self.school_record_last_year,
            self.school_record_three_years_ago,
            self.exam_score_this_year,
            self.exam_score_last_year,
            self.exam_score_three_years_ago,
            self.s_score_this_year,
            self.school_record_last_year,
            self.s_score_three_years_ago,
            self.border_this_year,
            self.border_last_year,
            self.border_three_years_ago,
            self.access
        ]


class FuturePath(models.Model):
    student_id = models.IntegerField(primary_key=True)
    first_choice = models.ForeignKey(PublicHighSchool, on_delete=models.SET_DEFAULT, default=0, related_name='first')
    first_situation = models.CharField(max_length=5, null=True)
    second_choice = models.ForeignKey(PublicHighSchool, on_delete=models.SET_DEFAULT, default=0, related_name='second')
    second_situation = models.CharField(max_length=5, null=True)
    third_choice = models.ForeignKey(PublicHighSchool, on_delete=models.SET_DEFAULT, default=0, related_name='third')
    third_situation = models.CharField(max_length=5, null=True)
    private_school1 = models.ForeignKey(PrivateHighSchool, on_delete=models.SET_DEFAULT, default=0, related_name='first')
    private_school2 = models.ForeignKey(PrivateHighSchool, on_delete=models.SET_DEFAULT, default=0, related_name='second')
    private_school3 = models.ForeignKey(PrivateHighSchool, on_delete=models.SET_DEFAULT, default=0, related_name='third')
    information = models.TextField(max_length=1000, null=True)
    record_date = models.DateField()

    def to_string(self):
        return {
            'first': self.first_choice.name,
            'second': self.second_choice.name,
            'third': self.third_choice.name,
            'private_school1': self.private_school1.name,
            'private_school2': self.private_school2.name,
            'private_school3': self.private_school3.name,
        }

    def get_public_schools(self):
        return {
            'first': self.first_choice,
            'second': self.second_choice,
            'third': self.third_choice,
        }

    def get_private_schools(self):
        return {
            'first': self.private_school1,
            'second': self.private_school2,
            'third': self.private_school3,
        }


def make_future_path(student_id):
    future_path = FuturePath(
        student_id=student_id,
        record_date=datetime.date.today()
    )
    future_path.save()
