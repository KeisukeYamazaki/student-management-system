# Generated by Django 3.0.4 on 2020-03-22 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registry', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='practiceexam',
            name='dev_five',
            field=models.CharField(max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='practiceexam',
            name='dev_three',
            field=models.CharField(max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='practiceexam',
            name='english_deviation',
            field=models.CharField(max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='practiceexam',
            name='english_score',
            field=models.CharField(max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='practiceexam',
            name='japanese_deviation',
            field=models.CharField(max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='practiceexam',
            name='japanese_score',
            field=models.CharField(max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='practiceexam',
            name='math_deviation',
            field=models.CharField(max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='practiceexam',
            name='math_score',
            field=models.CharField(max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='practiceexam',
            name='science_deviation',
            field=models.CharField(max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='practiceexam',
            name='science_score',
            field=models.CharField(max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='practiceexam',
            name='social_deviation',
            field=models.CharField(max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='practiceexam',
            name='social_score',
            field=models.CharField(max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='practiceexam',
            name='sum_all',
            field=models.CharField(max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='practiceexam',
            name='sum_three',
            field=models.CharField(max_length=5, null=True),
        ),
    ]
