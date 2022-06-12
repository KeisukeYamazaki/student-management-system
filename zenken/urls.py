from django.urls import path

from zenken.views import zenken_top

app_name = 'zenken'


urlpatterns = [
    path('', zenken_top, name='top'),
    path('edit/', zenken_top, name='edit'),
    path('download/', zenken_top, name='download'),
]
