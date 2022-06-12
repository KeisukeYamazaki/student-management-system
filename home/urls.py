from django.urls import path

from home.views import HomeView
from home.views import Login
from home.views import Logout

app_name = 'home'


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
]

