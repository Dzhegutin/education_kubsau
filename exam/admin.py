from django.contrib import admin
from .models import User, Subject, Task, UserAnswer

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'organization', 'profession')

class SubjectAdmin(admin.ModelAdmin):
    list_display = ('subject',)

class TaskAdmin(admin.ModelAdmin):
    list_display = ('subject', 'task_author', 'task_content', 'correct_answer', 'task_hint')

class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'task', 'user_response', 'is_correct', 'timestamp')



admin.site.register(User, UserAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(UserAnswer, UserAnswerAdmin)