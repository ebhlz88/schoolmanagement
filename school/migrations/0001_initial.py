# Generated by Django 3.2.8 on 2021-11-30 01:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='enroll_student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_enrollinstandard', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='schoolclasses',
            fields=[
                ('classid', models.BigAutoField(primary_key=True, serialize=False)),
                ('standardname', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='subjects',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subjectname', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='teacherdetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('t_name', models.CharField(max_length=50)),
                ('t_fname', models.CharField(max_length=50)),
                ('teacher_pic', models.ImageField(blank=True, upload_to='teacherpic')),
                ('dob', models.DateField()),
                ('m_number', models.CharField(max_length=20)),
                ('t_email', models.CharField(max_length=50)),
                ('date_hiring', models.DateField()),
                ('c_position', models.BooleanField(default=True)),
                ('sex', models.CharField(max_length=7)),
                ('address', models.CharField(max_length=200)),
                ('salary', models.IntegerField()),
                ('speciality', models.CharField(max_length=200)),
                ('bloodgroup', models.CharField(max_length=4, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='teachpaymonths',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teacheramount', models.IntegerField(default=0, null=True)),
                ('date_payed', models.DateField(auto_now_add=True)),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.teacherdetail')),
            ],
        ),
        migrations.CreateModel(
            name='studentsdetail',
            fields=[
                ('rollnbr', models.BigAutoField(primary_key=True, serialize=False)),
                ('student_pic', models.ImageField(blank=True, upload_to='studentpic')),
                ('s_name', models.CharField(max_length=50)),
                ('s_fname', models.CharField(max_length=50)),
                ('dob', models.DateField()),
                ('date_join', models.DateField()),
                ('c_position', models.BooleanField(default=True)),
                ('sex', models.CharField(max_length=7)),
                ('address', models.CharField(max_length=200)),
                ('fm_number', models.CharField(max_length=15)),
                ('bloodgroup', models.CharField(max_length=4)),
                ('currentStandard', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='school.schoolclasses')),
            ],
        ),
        migrations.CreateModel(
            name='marks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subjectmarks', models.PositiveSmallIntegerField(default=0, null=True)),
                ('enrollstudent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.enroll_student')),
                ('subjectname', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='school.subjects')),
            ],
        ),
        migrations.CreateModel(
            name='fees',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('studentamount', models.IntegerField(default=0, null=True)),
                ('date_enroll', models.DateField(auto_now_add=True)),
                ('enrollstudent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.enroll_student')),
            ],
        ),
        migrations.AddField(
            model_name='enroll_student',
            name='standard',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.schoolclasses'),
        ),
        migrations.AddField(
            model_name='enroll_student',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.studentsdetail'),
        ),
        migrations.CreateModel(
            name='books',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bookthumbnail', models.ImageField(blank=True, upload_to='books')),
                ('bookname', models.CharField(max_length=200)),
                ('book', models.FileField(upload_to='books')),
                ('standard', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.schoolclasses')),
            ],
        ),
    ]
