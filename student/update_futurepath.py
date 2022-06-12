
from app_base import *
from student.models import FuturePath

logger = getLogger(__name__)


def update_or_create_future_path(student, future_path, data):
    """update_or_create_future_path

        進路情報があれば入力情報に更新し、なければ新規作成を行う

        Args:
            student(Student): Studentのインスタンス
            future_path(future_path): future_pathのインスタンス
            data(dict): future_pathのフォーム入力情報のデータ

        Returns:
           True(登録・更新成功) or False(登録・更新失敗)
    """
    try:
        if future_path:
            logger.info(f'進路情報[更新]開始：{student.last_name} {student.first_name}')
            future_path.first_choice_id = data['first_choice']
            future_path.second_choice_id = data['second_choice']
            future_path.third_choice_id = data['third_choice']
            future_path.private_school1_id = data['private_school1']
            future_path.private_school2_id = data['private_school2']
            future_path.private_school3_id = data['private_school3']
            future_path.information = data['information']
            future_path.record_date = today
            future_path.save()
            return True
        else:
            logger.info(f'進路情報[登録]開始：{student.last_name} {student.first_name}')
            new_future_path = FuturePath(
                student_id=student.id,
                first_choice_id=data['first_choice'],
                second_choice_id=data['second_choice'],
                third_choice_id=data['third_choice'],
                private_school1_id=data['private_school1'],
                private_school2_id=data['private_school2'],
                private_school3_id=data['private_school3'],
                information=data['information'],
                record_date=today,
            )
            new_future_path.save()
            return True
    except:
        return False
