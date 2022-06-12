# Generated by Django 3.0.4 on 2020-03-28 01:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registry', '0007_gradeidlink'),
    ]

    operations = [
        migrations.CreateModel(
            name='PracticeMonth',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='RegularExamGroup',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=10)),
            ],
        ),
        migrations.AlterField(
            model_name='practiceexam',
            name='month',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='regularexam',
            name='regular_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='schoolrecord',
            name='term_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='registry.RecordGroup'),
        ),
    ]
