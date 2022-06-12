from django.contrib.auth import user_logged_in
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.dispatch import receiver
from django.views.generic import TemplateView

from app_base import *
from home.forms import LoginForm
from home.sql import get_birthday_sql
from student.models import Student
from student.models import HomeRoom

logger = getLogger(__name__)


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 誕生日の表示
        sql = get_birthday_sql().format("'" + str(today.month) + "'", "'" + str(today.month + 1) + "'")
        context['students'] = Student.objects.raw(sql)
        context['birthday_title'] = '{0}月と{1}月の誕生日'.format(str(today.month), str(today.month + 1))
        context['user'] = self.request.user
        # 各クラスの人数の表示
        # 中学部
        context['home_rooms_j'] = {}
        home_rooms = HomeRoom.objects.filter(grade__contains='中')
        junior_high_schools = {
            'seya': '瀬谷中',
            'shimochu': '下瀬谷中',
            'kochu': '光丘中',
            'azumano': '東野中',
            'nanchu': '南瀬谷中',
            'wachu': '大和中',
            'okazu': 'okazu',
        }
        for home_room in home_rooms:
            student_sum = 0
            context['home_rooms_j'][home_room.name] = {}
            # クラスの総数を取得
            context['home_rooms_j'][home_room.name]['sum'] = Student.objects.filter(home_room=home_room.name).count()
            # 学年を取得
            grade = HomeRoom.objects.get(name=home_room.name).grade
            for key, value in junior_high_schools.items():
                # 中学ごとの人数を取得
                context['home_rooms_j'][home_room.name][key] = Student.objects.filter(
                    local_school=value, grade=grade, home_room=home_room.name).count()
                # その中学の人数を合計に加える
                student_sum += context['home_rooms_j'][home_room.name][key]
            # クラスの総数からこれまでの合計を引いて、その他の中学の人数を算出
            context['home_rooms_j'][home_room.name]['others'] = context[
                                                                    'home_rooms_j'][home_room.name]['sum'] - student_sum
        # 小学部
        context['home_rooms_e'] = {}
        home_rooms = HomeRoom.objects.filter(grade__contains='小')
        junior_high_schools = {
            'daimon': '大門小',
            'daini': '瀬谷第二小',
            'kamiseya': '上瀬谷小',
            'sakura': '瀬谷さくら小',
            'seya': '瀬谷小',
            'aizawa': '相沢小',
            'hutatsu': '二ツ橋小',
        }
        for home_room in home_rooms:
            student_sum = 0
            context['home_rooms_e'][home_room.name] = {}
            # クラスの総数を取得
            context['home_rooms_e'][home_room.name]['sum'] = Student.objects.filter(home_room=home_room.name).count()
            # 学年を取得
            grade = HomeRoom.objects.get(name=home_room.name).grade
            for key, value in junior_high_schools.items():
                # 中学ごとの人数を取得
                context['home_rooms_e'][home_room.name][key] = Student.objects.filter(
                    local_school=value, grade=grade, home_room=home_room.name).count()
                # その中学の人数を合計に加える
                student_sum += context['home_rooms_e'][home_room.name][key]
            # クラスの総数からこれまでの合計を引いて、その他の中学の人数を算出
            context['home_rooms_e'][home_room.name]['others'] = context[
                                                                    'home_rooms_e'][home_room.name]['sum'] - student_sum

        return context


class Login(LoginView):
    """ログインページ"""
    form_class = LoginForm
    template_name = 'home/login.html'


class Logout(LogoutView):
    """ログアウトページ"""
    template_name = 'home/logout.html'


@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    """ログインした際に呼ばれる"""
    logger.info(f'ログイン：{user.username}（{datetime.datetime.now()})')
