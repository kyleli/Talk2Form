# Generated by Django 4.2.1 on 2023-06-17 06:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0008_alter_settings_ai_model_id_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Settings',
            new_name='FormSettings',
        ),
    ]