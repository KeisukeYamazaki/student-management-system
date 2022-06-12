from registry.models import SchoolRecord
from student.models import JuniorHighSchool
from zenken.logic import convert_gender
from zenken.logic import convert_city
from zenken.logic import convert_term


class ZenkenDelivery:
    def __init__(self, student, zenken=None):
        if zenken:
            self.student = student
            self.student_id = student.id
            self.number = int(zenken.zenken_number)
            self.gender = convert_gender(zenken.gender)
            self.name = student.last_name + ' ' + student.first_name
            self.name_ruby = student.last_ruby + ' ' + student.first_ruby
            self.city = convert_city(zenken.city)
            self.term = convert_term(zenken.recordTerm)
            self.school_records = self.get_school_record()
        else:
            self.student = student
            self.student_id = student.id
            self.number = None
            self.gender = None
            self.name = student.last_name + ' ' + student.first_name
            self.name_ruby = student.last_ruby + ' ' + student.first_ruby
            self.city = None
            self.term = JuniorHighSchool.objects.get(name=self.student.local_school).term
            self.school_records = self.get_school_record()

    def get_school_record(self):
        record_dict = {}
        grade = self.student.grade
        if grade == '中３':
            # 中３の場合、表示させる成績は「２年学年末(=record1)」「３年１学期(前期=record2)」「３年２学期(後期=record3)」
            if self.term == '３学期制':
                # すべて first() として、存在しない場合はNoneを代入する
                record_dict['record1'] = SchoolRecord.objects.filter(student_id=self.student_id,
                                                                     grade='中２',
                                                                     term_name_id=5).first()
                record_dict['record2'] = SchoolRecord.objects.filter(student_id=self.student_id,
                                                                     grade='中３',
                                                                     term_name_id=1).first()
                record_dict['record3'] = SchoolRecord.objects.filter(student_id=self.student_id,
                                                                     grade='中３',
                                                                     term_name_id=3).first()
            if self.term == '２学期制':
                record_dict['record1'] = SchoolRecord.objects.filter(student_id=self.student_id,
                                                                     grade='中２',
                                                                     term_name_id=4).first()
                record_dict['record2'] = SchoolRecord.objects.filter(student_id=self.student_id,
                                                                     grade='中３',
                                                                     term_name_id=2).first()
                record_dict['record3'] = SchoolRecord.objects.filter(student_id=self.student_id,
                                                                     grade='中３',
                                                                     term_name_id=4).first()
        elif grade == '中２':
            # 中２の場合、表示させる成績は「１年学年末(=record1)」「２年１学期(=record2)」「２年２学期(前期)(=record3)」
            if self.term == '３学期制':
                record_dict['record1'] = SchoolRecord.objects.filter(student_id=self.student_id,
                                                                     grade='中１',
                                                                     term_name_id=5).first()
                record_dict['record2'] = SchoolRecord.objects.filter(student_id=self.student_id,
                                                                     grade='中２',
                                                                     term_name_id=1).first()
                record_dict['record3'] = SchoolRecord.objects.filter(student_id=self.student_id,
                                                                     grade='中２',
                                                                     term_name_id=3).first()
            if self.term == '２学期制':
                record_dict['record1'] = SchoolRecord.objects.filter(student_id=self.student_id,
                                                                     grade='中１',
                                                                     term_name_id=4).first()
                record_dict['record2'] = None
                record_dict['record3'] = SchoolRecord.objects.filter(student_id=self.student_id,
                                                                     grade='中２',
                                                                     term_name_id=2).first()
        elif grade == '中１':
            # 中１の場合、表示させる成績は「１年１学期(=record1)」「１年２学期(前期)(=record2)」「１年３学期(後期)(=record3)」
            if self.term == '３学期制':
                record_dict['record1'] = SchoolRecord.objects.filter(student_id=self.student_id,
                                                                     grade='中１',
                                                                     term_name_id=1).first()
                record_dict['record2'] = SchoolRecord.objects.filter(student_id=self.student_id,
                                                                     grade='中１',
                                                                     term_name_id=3).first()
                record_dict['record3'] = SchoolRecord.objects.filter(student_id=self.student_id,
                                                                     grade='中１',
                                                                     term_name_id=5).first()
            if self.term == '２学期制':
                record_dict['record1'] = None
                record_dict['record2'] = SchoolRecord.objects.filter(student_id=self.student_id,
                                                                     grade='中１',
                                                                     term_name_id=2).first()
                record_dict['record3'] = SchoolRecord.objects.filter(student_id=self.student_id,
                                                                     grade='中１',
                                                                     term_name_id=4).first()
        return record_dict

    def __lt__(self, other):
        return self.number < other.number
