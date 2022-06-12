from django.db import models


class Zenken(models.Model):
    student_id = models.IntegerField(primary_key=True)
    zenken_number = models.CharField(max_length=10, null=True)
    gender = models.CharField(max_length=5, null=True)
    enrollment = models.CharField(max_length=5, null=True)
    prefecture = models.CharField(max_length=5, null=True)
    city = models.CharField(max_length=5, null=True)
    recordTerm = models.CharField(max_length=5, null=True)
