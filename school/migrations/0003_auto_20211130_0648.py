# Generated by Django 3.2.8 on 2021-11-30 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0002_alter_studentsdetail_rollnbr'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schoolclasses',
            name='classid',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='studentsdetail',
            name='rollnbr',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]