from django.contrib import admin

from student.models import HomeRoom
from student.models import ElementarySchool
from student.models import JuniorHighSchool

admin.site.register(HomeRoom)
admin.site.register(ElementarySchool)
admin.site.register(JuniorHighSchool)

