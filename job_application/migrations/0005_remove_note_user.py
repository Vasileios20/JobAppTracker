# Generated by Django 4.2.7 on 2024-10-16 12:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job_application', '0004_note_delete_jobnotes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='note',
            name='user',
        ),
    ]
