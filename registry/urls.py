from django.urls import path

from registry.views import registry_home
from registry.views import registry_school_record
from registry.views import registry_regular_exam
from registry.views import registry_practice_exam
from registry.views import registry_personal

app_name = 'registry'


urlpatterns = [
    path('', registry_home, name='home'),
    path('school-record/', registry_school_record, name='school-record'),
    path('school-record/<str:grade>/', registry_school_record, name='school-record'),
    path('regular-exam/', registry_regular_exam, name='regular-exam'),
    path('practice-exam/', registry_practice_exam, name='practice-exam'),
    path('practice-exam/<str:kind>/', registry_practice_exam, name='practice-exam'),
    path('personal/', registry_personal, name='personal'),
    path('personal/<str:grade>/', registry_personal, name='personal'),
    path('personal/<str:grade>/<int:pk>/', registry_personal, name='personal'),
    path('personal/<str:grade>/<int:pk>/<str:kind>/', registry_personal, name='personal'),
]
