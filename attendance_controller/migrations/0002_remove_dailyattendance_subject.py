# Generated by Django 2.1 on 2019-09-10 08:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance_controller', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dailyattendance',
            name='subject',
        ),
    ]
