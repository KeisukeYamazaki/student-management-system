import os
from logging import getLogger

import openpyxl

from download.meeting_sheet_classes import MeetingSheet3rd2nd
from download.meeting_sheet_classes import MeetingSheet1st
from student.exam_record import ExamRecord
from student.models import JuniorHighSchool

logger = getLogger(__name__)


def make_excel_meeting_sheet(file_name, student, record_list, r_exam_list, this_grade_exam_list, last_grade_exam,
                             public_school_dict, calc_score_dict, score_dict, private_school_dict):
    """make_excel_meeting_sheet

        エクセルで面談シートを作成する

        Args:
            file_name (str): ファイル名
            student (Student): Studentインスタンス
            record_list (list): SchoolRecordを格納したリスト
            r_exam_list (list): RegularExamを格納したリスト
            this_grade_exam_list (list): 今年度のPracticeExamを格納したdict
            last_grade_exam (PracticeExam) : 昨年度最終のPracticeExamインスタンス(中２、中３)
            public_school_dict (dict): PublicHighSchoolを格納したリスト
            calc_score_dict (dict): 平均内申までの差、目標点、ボーダー点のdict
            score_dict (dict): 合格者平均内申、合格者平均得点、ボーダー点のdict
            private_school_dict (dict): PrivateHighSchoolを格納したdict
    """
    # ３学期制か２学期制か
    term_system = JuniorHighSchool.objects.get(name=student.local_school).term
    logger.info(term_system)
    # 学年・学期制からシート名の選択・ループカウントの代入
    if student.grade == '中３':
        logger.info('中３')
        loop_count = 3
        now_grade = 3
        if term_system == '３学期制':
            sheet_name = 'meetingSheet_3rd3term'
        elif term_system == '２学期制':
            sheet_name = 'meetingSheet_3rd2term'
    elif student.grade == '中２':
        logger.info('中２')
        loop_count = 2
        now_grade = 2
        if term_system == '３学期制':
            sheet_name = 'meetingSheet_2nd3term'
        elif term_system == '２学期制':
            sheet_name = 'meetingSheet_2nd2term'
    elif student.grade == '中１':
        logger.info('中１')
        loop_count = 1
        now_grade = 1
        if term_system == '３学期制':
            sheet_name = 'meetingSheet_1st3term'
        elif term_system == '２学期制':
            sheet_name = 'meetingSheet_1st2term'
    # テンプレートファイルを取得し、シートを展開
    base_path = os.getcwd()
    file_path = f'/download/excel/meeting_sheet/{sheet_name}.xlsx'
    wb = openpyxl.load_workbook(base_path + file_path)
    ws = wb.worksheets[0]
    # テンプレートクラスを取得・学年によって処理が変わるものの処理
    exam_record = ExamRecord(student)
    if student.grade == '中１':
        template = MeetingSheet1st(ws, student)
        logger.info('中１テンプレートファイル取得')
        # 模試結果の書き込み
        template.set_practice_exam(this_grade_exam_list, exam_record)
        logger.info('中１模試結果書き込み完了')
        # 公立高校の書き込み(第一志望がなければ書き込みしない）
        template.set_public_school(public_school_dict, score_dict, calc_score_dict)
    else:
        template = MeetingSheet3rd2nd(ws, student)
        # A値の書き込み
        template.set_A_value()
        # 模試結果の書き込み
        template.set_practice_exam(this_grade_exam_list, exam_record, last_grade_exam)
        # 公立高校の書き込み(第一志望がなければ書き込みしない）
        if not len(calc_score_dict) == 0:
            template.set_public_school(public_school_dict, calc_score_dict)
    # 学年問わず共通の処理
    # 内申・定期試験の書き込み
    list_num = 0
    for write_grade in range(1, loop_count + 1):
        template.set_school_record(record_list[list_num], write_grade, now_grade)
        template.set_regular_exam(r_exam_list[list_num], write_grade, now_grade)
        list_num += 1
    # 私立高校の書き込み
    template.set_private_school(private_school_dict)

    # 作成
    wb.save(base_path + '/' + file_name)
