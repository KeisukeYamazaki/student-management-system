from django.urls import path

from download.views import download_home
from download.views import name_sheet_view
from download.views import meeting_sheet_view

app_name = 'download'


urlpatterns = [
    path('', download_home, name='home'),
    path('name-sheet/', name_sheet_view, name='name_sheet'),
    path('name-sheet/<str:kind>/', name_sheet_view, name='name_sheet'),
    path('meeting-sheet/', meeting_sheet_view, name='meeting_sheet'),
    path('meeting-sheet/<str:grade>/', meeting_sheet_view, name='meeting_sheet'),
    path('meeting-sheet/<str:grade>/<int:pk>/', meeting_sheet_view, name='meeting_sheet'),
]
