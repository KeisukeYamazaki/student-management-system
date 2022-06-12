from django.db import models


class UpdateRecord(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=50)
    date = models.DateField()

