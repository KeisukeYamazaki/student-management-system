# Generated by Django 3.0.4 on 2020-03-28 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0008_auto_20200328_1523'),
    ]

    operations = [
        migrations.AlterField(
            model_name='privatehighschool',
            name='standard_score',
            field=models.CharField(max_length=100, null=True),
        ),
    ]