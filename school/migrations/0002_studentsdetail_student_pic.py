# Generated by Django 3.2 on 2021-08-23 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentsdetail',
            name='student_pic',
            field=models.ImageField(default=0, upload_to='studentpic'),
            preserve_default=False,
        ),
    ]
