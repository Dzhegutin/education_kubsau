# Generated by Django 5.0.4 on 2024-05-17 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0003_task_task_name_alter_task_task_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='task_name',
            field=models.CharField(max_length=255),
        ),
    ]