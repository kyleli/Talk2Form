# Generated by Django 4.2.1 on 2023-06-15 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_question_editing'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='audiofile',
            name='file_path',
        ),
        migrations.AddField(
            model_name='audiofile',
            name='audio_file',
            field=models.FileField(default=None, upload_to='audio_files/'),
        ),
    ]