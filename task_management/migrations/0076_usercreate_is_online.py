# Generated by Django 4.2.6 on 2023-10-24 02:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_management', '0075_activity_task'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercreate',
            name='is_online',
            field=models.BooleanField(default=False),
        ),
    ]
