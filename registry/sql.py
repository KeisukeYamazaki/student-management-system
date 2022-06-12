from django.db import connection

from registry.models import GradeIdLink


def dict_fetch_all(cursor):
    """Return all rows from a cursor as a dict"""
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def get_school_records(now_grade, select_grade, term_name):
    start_id = GradeIdLink.objects.get(grade=now_grade).start_id
    if term_name == '１学期・前期':
        condition = "(registry_schoolrecord.term_name_id = 1 OR registry_schoolrecord.term_name_id = 2)"
    elif term_name == '２学期':
        condition = "registry_schoolrecord.term_name_id = 3"
        condition2 = "term = '３学期制' AND"
    elif term_name == '２学期・後期':
        condition = \
            "(registry_schoolrecord.term_name_id = 3 OR registry_schoolrecord.term_name_id = 4)"
    elif term_name == '３学期・後期':
        condition = \
            "(registry_schoolrecord.term_name_id = 4 OR registry_schoolrecord.term_name_id = 5)"

    if term_name == '２学期':
        sql = school_record_base_sql(now_grade, select_grade, condition, start_id, term=condition2)
    else:
        sql = school_record_base_sql(now_grade, select_grade, condition, start_id)

    with connection.cursor() as cursor:
        cursor.execute(sql)
        return dict_fetch_all(cursor)


def school_record_base_sql(now_grade, select_grade, condition, start_id, term=''):
    sql = """
            SELECT
                student_student.id AS student_id,
                student_student.last_name,
                student_student.first_name,
                registry_schoolrecord.id AS record_id,
                registry_schoolrecord.grade AS record_grade,
                record_year,
                registry_recordgroup.term_name,
                english,
                math,
                japanese,
                science,
                social_studies,
                music,
                art,
                pe,
                tech_home,
                student_juniorhighschool.term
            FROM
                student_student
            LEFT OUTER JOIN registry_schoolrecord ON
                student_student.id = registry_schoolrecord.student_id
                AND student_student.grade = {now_grade}
                AND registry_schoolrecord.grade = {select_grade}
                AND {condition}
            LEFT OUTER JOIN registry_recordgroup ON
                registry_schoolrecord.term_name_id = registry_recordgroup.id
            JOIN student_juniorhighschool ON
                student_student.local_school = student_juniorhighschool.name
            WHERE 
                {condition_2nd_term}
                student_student.id BETWEEN {start_id} AND {end_id}
                AND student_student.id > 0
            ORDER BY
                student_student.id;
        """.format(
        now_grade="'" + now_grade + "'",
        select_grade="'" + select_grade + "'",
        condition=condition,
        condition_2nd_term=term,
        start_id=start_id,
        end_id=start_id + 98,
    )
    # now_grade と start_id, end_id が対応
    return sql
