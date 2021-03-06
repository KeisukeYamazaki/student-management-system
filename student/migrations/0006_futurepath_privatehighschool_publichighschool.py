# Generated by Django 3.0.4 on 2020-03-28 05:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0005_homeroom'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrivateHighSchool',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('course', models.CharField(max_length=20, null=True)),
                ('exam_way', models.CharField(max_length=20, null=True)),
                ('document_selection', models.NullBooleanField()),
                ('boys_or_girls_only', models.CharField(max_length=5, null=True)),
                ('standard_score', models.CharField(max_length=10, null=True)),
                ('add_point', models.CharField(max_length=200, null=True)),
                ('score_percentage', models.IntegerField(null=True)),
                ('features', models.CharField(max_length=100, null=True)),
                ('commuting_time', models.IntegerField(null=True)),
                ('using_bus', models.NullBooleanField()),
                ('remarks', models.CharField(max_length=100, null=True)),
                ('access', models.CharField(max_length=75, null=True)),
                ('update_date', models.DateField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PublicHighSchool',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('score_ratio', models.CharField(max_length=10, null=True)),
                ('school_report_this_year', models.CharField(max_length=10, null=True)),
                ('school_report_last_year', models.CharField(max_length=10, null=True)),
                ('school_report_three_years_ago', models.CharField(max_length=10, null=True)),
                ('exam_score_this_year', models.CharField(max_length=10, null=True)),
                ('exam_score_last_year', models.CharField(max_length=10, null=True)),
                ('exam_score_three_years_ago', models.CharField(max_length=10, null=True)),
                ('s_score_this_year', models.CharField(max_length=10, null=True)),
                ('s_score_last_year', models.CharField(max_length=10, null=True)),
                ('s_score_three_years_ago', models.CharField(max_length=10, null=True)),
                ('border_this_year', models.CharField(max_length=10, null=True)),
                ('border_last_year', models.CharField(max_length=10, null=True)),
                ('border_three_years_ago', models.CharField(max_length=10, null=True)),
                ('second_border_this_year', models.CharField(max_length=10, null=True)),
                ('second_border_last_year', models.CharField(max_length=10, null=True)),
                ('second_border_three_years_ago', models.CharField(max_length=10, null=True)),
                ('competition_rate_this_year', models.CharField(max_length=10, null=True)),
                ('competition_rate_last_year', models.CharField(max_length=10, null=True)),
                ('competition_rate_three_years_ago', models.CharField(max_length=10, null=True)),
                ('extra1', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='extra1', to='student.PrivateHighSchool')),
                ('extra2', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='extra2', to='student.PrivateHighSchool')),
                ('extra3', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='extra3', to='student.PrivateHighSchool')),
                ('extra4', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='extra4', to='student.PrivateHighSchool')),
                ('extra5', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='extra5', to='student.PrivateHighSchool')),
                ('access', models.CharField(max_length=75, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FuturePath',
            fields=[
                ('student_id', models.IntegerField(primary_key=True, serialize=False)),
                ('first_choice', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='first', to='student.PublicHighSchool')),
                ('first_situation', models.CharField(max_length=5, null=True)),
                ('second_choice', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='second', to='student.PublicHighSchool')),
                ('second_situation', models.CharField(max_length=5, null=True)),
                ('third_choice', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='third', to='student.PublicHighSchool')),
                ('third_situation', models.CharField(max_length=5, null=True)),
                ('private_school1', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='first', to='student.PrivateHighSchool')),
                ('private_school2', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='second', to='student.PrivateHighSchool')),
                ('private_school3', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='third', to='student.PrivateHighSchool')),
                ('information', models.TextField(max_length=1000, null=True)),
                ('record_date', models.DateField()),
            ],
        ),
    ]
