# Generated by Django 3.0.4 on 2020-04-19 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0010_auto_20200405_1116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='elementaryschool',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='juniorhighschool',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
