# Generated by Django 2.2.3 on 2019-07-29 21:02

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('qa', '0003_answermodel'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AnswerModel',
            new_name='Answer',
        ),
    ]
