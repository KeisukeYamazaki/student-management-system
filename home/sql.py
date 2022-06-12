
def get_birthday_sql():
    sql = """
          SELECT * FROM student_student 
          WHERE to_char(birthday, 'FMMM') = {0} AND id > 0
                OR to_char(birthday, 'FMMM') = {1} AND id > 0
          ORDER BY to_char(birthday, 'MM-dd')
          """
    return sql
