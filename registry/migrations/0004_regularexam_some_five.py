# Generated by Django 3.0.4 on 2020-03-22 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registry', '0003_remove_regularexam_exam_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='regularexam',
            name='some_five',
            field=models.CharField(max_length=5, null=True),
        ),
    ]
