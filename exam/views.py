# Create your views here.
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from .forms import SignUpForm

from django.contrib import messages

from .models import User, Subject, Task


def registration(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')
            if password1 == password2:
                form.save()
                messages.success(request, 'Регистрация прошла успешно. Пожалуйста, войдите в свой аккаунт.')
                return redirect('success_login')  # Перенаправляем на страницу успешной регистрации
            else:
                form.add_error('password2', "Пароли не совпадают")  # Добавляем ошибку к полю "Подтвердить пароль"
    else:
        form = SignUpForm()
    return render(request, 'exam/login.html', {'form': form})

def success_login(request):
    return render(request, 'exam/success_login.html')



def my_tests(request):
    yourTask.objects.all()

    return render(request, 'exam/my_tests.html')

def forgot_pass(request):
    return render(request, 'exam/forgot_pass.html')

def pass_reset(request):
    return render(request, 'exam/pass_reset.html')

def code(request):
    return render(request, 'exam/code.html')

class LoginView(View):
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Вход выполнен успешно, перенаправляем на нужную страницу
            return redirect('success_login')
        else:
            # Неверные учетные данные, отображаем форму входа с сообщением об ошибке
            return render(request, 'exam/login.html', {'error_message': 'Неверное имя пользователя или пароль.'})

def my_authors(request):
    return render(request, 'exam/my_authors.html')

def my_acc(request):
    users = User.objects.all()
    return render(request, 'exam/my_acc.html', {'users': users})

from django.http import JsonResponse

def update_profile(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.profession = request.POST.get('profession')
        user.organization = request.POST.get('organization')
        user.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})

def update_avatar(request):
    if request.method == 'POST':
        user = request.user
        avatar = request.FILES.get('avatar')
        if avatar:
            user.photo = avatar
            user.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'No avatar provided'}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)


def create_test(request):
    if request.method == 'POST':
        subject_id = request.POST['subject']
        task_name = request.POST['task_name']
        subject = Subject.objects.get(id=subject_id)

        # Создаем объект теста
        task_author = request.user
        # new_task = Task(
        #     subject=subject,
        #     task_author=task_author,
        #     task_name=task_name,
        # )
        # new_task.save()

        # Добавляем задания к тесту
        task_contents = request.POST.getlist('task_content')
        correct_answers = request.POST.getlist('correct_answer')
        wrong_1s = request.POST.getlist('wrong_1')
        wrong_2s = request.POST.getlist('wrong_2')
        wrong_3s = request.POST.getlist('wrong_3')
        task_hints = request.POST.getlist('task_hint')

        for i in range(len(task_contents)):
            Task.objects.create(
                subject=subject,
                task_author=task_author,
                task_name=task_name,
                task_content=task_contents[i],
                correct_answer=correct_answers[i],
                wrong_1=wrong_1s[i],
                wrong_2=wrong_2s[i],
                wrong_3=wrong_3s[i],
                task_hint=task_hints[i]
            )
        return render(request, 'exam/success_login.html')

        # return redirect('exam/success_login.html')

    subjects = Subject.objects.all()
    print(subjects)
    return render(request, 'exam/create_test.html', {'subjects': subjects})


def check_task_name(request):
    task_name = request.GET.get('task_name')
    exists = Task.objects.filter(task_name=task_name).exists()
    return JsonResponse({'exists': exists})