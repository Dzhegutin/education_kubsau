import uuid

from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    organization = models.CharField(max_length=255)
    profession = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='user_photos/', blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.organization})"


class Subject(models.Model):
    subject = models.CharField(max_length=255)

    def __str__(self):
        return self.subject


class Task(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    task_author = models.ForeignKey('User', on_delete=models.CASCADE)
    task_name = models.CharField(max_length=255)
    task_content = models.TextField()
    task_photo = models.ImageField(upload_to=f'tasks/{task_name}/', blank=True, null=True)
    correct_answer = models.TextField()
    wrong_1 = models.TextField(blank=True, null=True)
    wrong_2 = models.TextField(blank=True, null=True)
    wrong_3 = models.TextField(blank=True, null=True)
    task_hint = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.task_name


class UserAnswer(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user_response = models.TextField()
    is_correct = models.BooleanField()
    timestamp = models.DateTimeField()
    session_key = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return f'{self.user.username} - {self.task.task_content}'

