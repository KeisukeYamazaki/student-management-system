import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from django.views.generic import UpdateView
from django.views.generic import FormView
from django.views.generic import DetailView
from django.views.generic import CreateView

from app_base import *
from student.models import make_future_path
from student.update_futurepath import update_or_create_future_path
from util import convert_grade, expireEncoda
from registry.models import SchoolRecord
from registry.models import RegularExam
from registry.models import PracticeExam
from student.exam_record import ExamRecord
from student.forms import StudentUpdateForm
from student.forms import StudentCreateForm
from student.models import Student
from student.models import PublicHighSchool
from student.models import PrivateHighSchool
from student.models import HomeRoom
from student.models import ElementarySchool
from student.models import JuniorHighSchool
from student.models import FuturePath

grade_list = ['中３', '中２', '中１', '小６', '小５', '小４', '小３']
grade_values = ['j3', 'j2', 'j1', 'e6', 'e5', 'e4', 'e3']

logger = getLogger(__name__)


class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    queryset = Student.objects.order_by('home_room', 'id')
    login_url = '/login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        count_list = []
        for grade in grade_list:
            count_list.append(Student.objects.filter(grade__exact=grade).filter(id__gte=0).count())
        context['count_list'] = count_list
        context['count_all'] = sum(count_list)
        return context


class StudentDetailView(LoginRequiredMixin, DetailView):
    model = Student
    login_url = '/login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        junior_grade_list = ['中１', '中２', '中３']

        context['school_records'] = {}
        context['regular_exams'] = {}
        context['practice_exams'] = {}

        id = self.object.id
        for i in range(3):
            if i == 0:
                g = '中学１年'
            elif i == 1:
                g = '中学２年'
            else:
                g = '中学３年'

            grade = junior_grade_list[i]
            context['school_records'][g] = SchoolRecord.objects.filter(student_id=id, grade=grade).order_by('term_name')
            context['regular_exams'][g] = RegularExam.objects.filter(student_id=id, grade=grade).order_by('regular_id')
            context['practice_exams'][g] = PracticeExam.objects.filter(student_id=id, grade=grade).order_by('month')

        try:
            context['future_path'] = FuturePath.objects.get(student_id=self.object.id)
        except ObjectDoesNotExist:
            make_future_path(self.object.id)
            context['future_path'] = FuturePath.objects.get(student_id=self.object.id)

        context['exam_record'] = ExamRecord(self.object)

        public_schools = context['future_path'].get_public_schools()
        keys = ['first', 'second', 'third']
        context['public_schools'] = {}
        context['public_schools_calc'] = {}
        for i in range(3):
            public_school = public_schools[keys[i]]
            if public_school:
                context['public_schools'][keys[i]] = public_school.get_data_all_kind()
                context['public_schools_calc'][keys[i]] = public_school.get_data_all_kind(context['exam_record'])

        context['private_schools'] = context['future_path'].get_private_schools()

        logger.info('生徒詳細：{} {} ({})〔user: {}〕'.format(
            self.object.last_name,
            self.object.first_name,
            self.object.grade,
            self.request.user
        ))

        return context


class StudentUpdateView(LoginRequiredMixin, UpdateView):
    model = Student
    form_class = StudentUpdateForm
    template_name = 'student/student_update_form.html'
    login_url = '/login'

    def get_success_url(self):
        return reverse('student:detail', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        result = super().form_valid(form)
        messages.success(self.request, '更新しました')
        logger.info('更新処理：{} {} ({})〔user: {}〕'.format(
            form.cleaned_data['last_name'],
            form.cleaned_data['first_name'],
            form.cleaned_data['grade'],
            self.request.user
        ))
        return result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if context['student'].birthday:
            context['birthday'] = context['student'].birthday.strftime('%Y-%m-%d')
        return context


class StudentCreateView(LoginRequiredMixin, CreateView):
    form_class = StudentCreateForm
    model = Student
    template_name = 'student/student_create_form.html'
    login_url = '/login'

    def get_success_url(self):
        messages.success(self.request, '登録しました')
        logger.info('新規登録：{} {} ({})〔user: {}〕'.format(
            self.object.last_name,
            self.object.first_name,
            self.object.grade,
            self.request.user
        ))
        own_grade = self.request.session['grade']
        del self.request.session['grade']
        if 'form' in self.request.session:
            del self.request.session['form']
        for i in range(len(grade_list)):
            if own_grade == grade_list[i]:
                tab = i + 1
                break

        return reverse('student:list', args=str(tab))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'grade' in self.kwargs.keys():
            context['grade'] = self.kwargs['grade']
            grade = convert_grade(context['grade'])
            context['japanese_grade'] = grade
            last_student = Student.objects.filter(grade=grade).order_by('id').last()
            context['student_id'] = last_student.id + 1
            context['grade_list'] = grade_list
            context['home_rooms'] = HomeRoom.objects.filter(grade=grade).values_list('name')
            if '小' in grade:
                context['local_schools'] = ElementarySchool.objects.values_list('name')
            else:
                context['local_schools'] = JuniorHighSchool.objects.values_list('name')

            if 'form' in self.request.session:
                context['session_data'] = self.request.session['form']

        return context

    def form_valid(self, form):
        ctx = {'form': form}
        if self.request.POST.get('next', '') == 'confirm':
            self.request.session['form'] = form.cleaned_data
            self.request.session['form']['birthday'] = json.dumps(form.cleaned_data['birthday'], default=expireEncoda)
            ctx['grade'] = convert_grade(form.cleaned_data['grade'])
            return render(self.request, 'student/create_confirm.html', ctx)
        if self.request.POST.get('next', '') == 'create':
            self.request.session['grade'] = form.cleaned_data['grade']
            return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class CreateConfirmView(LoginRequiredMixin, FormView):
    form_class = StudentCreateForm
    template_name = 'student/create_confirm.html'
    login_url = '/login'

    def form_valid(self, form):
        return render(self.request, 'student/student_create_form.html', {'form': form})

    def form_invalid(self, form):
        return render(self.request, 'student/student_create_form.html', {'form': form})


@login_required(login_url='login/')
@require_POST
def delete_student(request, pk):
    student = get_object_or_404(Student, id=pk)
    messages.success(request, '削除しました')
    logger.info('削除処理：{} {} ({})〔user: {}〕'.format(
        student.last_name,
        student.first_name,
        student.grade,
        request.user,
    ))
    own_grade = student.grade
    for i in range(len(grade_list)):
        if own_grade == grade_list[i]:
            tab = i + 1
            break
    student.delete()
    return redirect('student:list', tab)


@login_required(login_url='login/')
def class_management(request, **kwargs):
    form = {'grade_list': grade_list}

    if request.method == 'POST':
        data = dict(request.POST)
        for i in range(len(data['id'])):
            student_id = data['id'][i]
            student = Student.objects.get(id=student_id)
            student.home_room = data['home_room'][i]
            student.save()
        messages.success(request, '更新しました')
        logger.info('クラス変更：{}〔user: {}〕'.format(convert_grade(kwargs['grade']), request.user))
        return redirect('student:class', kwargs['grade'])

    if kwargs:
        grade = convert_grade(kwargs['grade'])
        students = Student.objects.filter(grade=grade, id__gte=0).order_by('home_room', 'id')
        home_rooms = HomeRoom.objects.filter(grade=grade).values_list('name')
        form['grade'] = kwargs['grade']
        form['students'] = students
        form['home_rooms'] = home_rooms

    return render(request, 'student/class_management.html', form)


@login_required(login_url='login/')
def future_path_update(request, **kwargs):
    future_path = FuturePath.objects.get(student_id=kwargs['pk'])
    student = Student.objects.get(id=kwargs['pk'])

    if request.method == 'POST':
        data = request.POST.dict()
        # update_future_pathメソッドで進路情報を登録・更新する(TrueかFalseが返る)
        result = update_or_create_future_path(student, future_path, data)
        if result:
            messages.success(request, '進路情報を更新しました')
            logger.info('進路情報変更：{} {}〔user: {}〕'.format(student.last_name, student.first_name, request.user))
        else:
            messages.error(request, '進路情報の更新に失敗しました')
            logger.error('進路情報変更 失敗：{} {}〔user: {}〕'.format(student.last_name, student.first_name, request.user))
        return redirect('student:detail', kwargs['pk'])

    context = {
        'future_path': future_path,
        'student': student,
        'public_high_schools': PublicHighSchool.objects.all(),
        'private_high_schools': PrivateHighSchool.objects.all(),
    }
    return render(request, 'student/future_path_update_form.html', context)


@login_required(login_url='login/')
def create_local_school(request):
    if request.method == 'POST':
        data = request.POST.dict()
        if data['school_kind'] == 'junior':
            school_name = data['name'] + '中'
            school = JuniorHighSchool(name=school_name, term=data['term'])
            school.save()
        elif data['school_kind'] == 'elementary':
            school_name = data['name'] + '小'
            school = ElementarySchool(name=school_name)
            school.save()

        messages.success(request, f'{school_name}を登録しました。このページを閉じてください。')
        logger.info(f'新規学校登録：{school_name} 〔user: {request.user}〕')

    return render(request, 'student/create_local_school.html')


@login_required(login_url='login/')
def create_local_school_ajax(request):
    # パラメータが渡ってきた場合、データベースの最終idの学校の名前をjsonで返す
    # 小学校の場合
    if 'elementary' in request.GET:
        e_school = ElementarySchool.objects.all().order_by('id').last().name
        return JsonResponse({'name': e_school})
    # 中学校の場合
    if 'junior' in request.GET:
        j_school = JuniorHighSchool.objects.all().order_by('id').last().name
        return JsonResponse({'name': j_school})

    junior = JuniorHighSchool.objects.all().count()
    elementary = ElementarySchool.objects.all().count()
    data = {
        'junior': junior,
        'elementary': elementary,
    }
    # JSONで返す
    return JsonResponse(data)
