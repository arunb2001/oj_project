# Generated by Django 4.0.5 on 2022-07-01 20:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('online_judge', '0003_alter_submission_timestamp'),
    ]

    operations = [
        migrations.RenameField(
            model_name='submission',
            old_name='problem_name',
            new_name='problemID',
        ),
        migrations.RenameField(
            model_name='submission',
            old_name='submitted_by',
            new_name='userID',
        ),
    ]
