from django.urls import path

from .views import StudentListView
from .views import StudentDetailView
from .views import StudentUpdateView
from .views import StudentCreateView
from .views import delete_student
from .views import class_management
from .views import future_path_update
from .views import create_local_school
from .views import create_local_school_ajax

app_name = 'student'


urlpatterns = [
    path('', StudentListView.as_view(), name='list'),
    path('<int:pk>', StudentListView.as_view(), name='list'),
    path('detail/<int:pk>/', StudentDetailView.as_view(), name='detail'),
    path('update/<int:pk>/', StudentUpdateView.as_view(), name='update'),
    path('future_path_update/<int:pk>/', future_path_update, name='future_path_update'),
    path('create/', StudentCreateView.as_view(), name='create'),
    path('create/school/', create_local_school, name='create_local_school'),
    path('create/school/ajax', create_local_school_ajax, name='create_local_school_ajax'),
    path('create/<str:grade>/', StudentCreateView.as_view(), name='create'),
    path('delete/<int:pk>/', delete_student, name='delete'),
    path('class/', class_management, name='class'),
    path('class/<str:grade>/', class_management, name='class'),
]
