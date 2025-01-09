# Generated by Django 5.1.4 on 2025-01-09 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_task_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='access_level',
            field=models.CharField(choices=[('public', 'Public'), ('private', 'Private')], default='public', max_length=10),
        ),
    ]
