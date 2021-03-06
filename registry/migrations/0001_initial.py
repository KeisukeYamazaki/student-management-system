# Generated by Django 3.0.4 on 2020-03-22 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PracticeExam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.IntegerField()),
                ('grade', models.CharField(max_length=10)),
                ('exam_year', models.IntegerField()),
                ('month', models.IntegerField(choices=[(1, '７月'), (2, '８月'), (3, '10月'), (4, '12月'), (5, '１月'), (6, '３月')])),
                ('english_score', models.IntegerField(null=True)),
                ('math_score', models.IntegerField(null=True)),
                ('japanese_score', models.IntegerField(null=True)),
                ('science_score', models.IntegerField(null=True)),
                ('social_score', models.IntegerField(null=True)),
                ('sum_three', models.IntegerField(null=True)),
                ('sum_all', models.IntegerField(null=True)),
                ('dev_three', models.IntegerField(null=True)),
                ('dev_five', models.IntegerField(null=True)),
                ('english_deviation', models.IntegerField(null=True)),
                ('math_deviation', models.IntegerField(null=True)),
                ('japanese_deviation', models.IntegerField(null=True)),
                ('science_deviation', models.IntegerField(null=True)),
                ('social_deviation', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RegularExam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.IntegerField()),
                ('grade', models.CharField(max_length=10)),
                ('exam_year', models.IntegerField()),
                ('exam_name', models.CharField(max_length=15)),
                ('regular_id', models.IntegerField(choices=[(1, '１学期中間'), (2, '前期中間'), (3, '１学期期末'), (4, '前期期末'), (5, '２学期中間'), (6, '後期中間'), (7, '２学期期末'), (8, '学年末')])),
                ('english', models.CharField(max_length=5, null=True)),
                ('math', models.CharField(max_length=5, null=True)),
                ('japanese', models.CharField(max_length=5, null=True)),
                ('science', models.CharField(max_length=5, null=True)),
                ('social_studies', models.CharField(max_length=5, null=True)),
                ('music', models.CharField(max_length=5, null=True)),
                ('art', models.CharField(max_length=5, null=True)),
                ('pe', models.CharField(max_length=5, null=True)),
                ('tech', models.CharField(max_length=5, null=True)),
                ('home', models.CharField(max_length=5, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SchoolRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.IntegerField()),
                ('grade', models.CharField(max_length=10)),
                ('record_year', models.IntegerField()),
                ('term_name', models.IntegerField(choices=[(1, '１学期'), (2, '前期'), (3, '２学期'), (4, '後期'), (5, '３学期')])),
                ('english', models.IntegerField(null=True)),
                ('math', models.IntegerField(null=True)),
                ('japanese', models.IntegerField(null=True)),
                ('science', models.IntegerField(null=True)),
                ('social_studies', models.IntegerField(null=True)),
                ('music', models.IntegerField(null=True)),
                ('art', models.IntegerField(null=True)),
                ('pe', models.IntegerField(null=True)),
                ('tech_home', models.IntegerField(null=True)),
                ('sum_five', models.IntegerField(null=True)),
                ('sum_all', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TimeLimit',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('sheet_name', models.CharField(max_length=10)),
            ],
        ),
        migrations.AddConstraint(
            model_name='schoolrecord',
            constraint=models.UniqueConstraint(fields=('student_id', 'grade', 'record_year', 'term_name'), name='record_const'),
        ),
        migrations.AddConstraint(
            model_name='regularexam',
            constraint=models.UniqueConstraint(fields=('student_id', 'grade', 'exam_year', 'regular_id'), name='regular_const'),
        ),
        migrations.AddConstraint(
            model_name='practiceexam',
            constraint=models.UniqueConstraint(fields=('student_id', 'grade', 'exam_year', 'month'), name='practice_const'),
        ),
    ]
