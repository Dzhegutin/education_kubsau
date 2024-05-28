# Create your views here.
import random
import uuid
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Count, ExpressionWrapper, FloatField, Q, Sum, Max
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views import View
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from .forms import SignUpForm

from django.contrib import messages

from .models import User, Subject, Task, UserAnswer


def main_page(request):
    return render(request, 'exam/main_page.html')


def auth(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')
            if password1 == password2:
                form.save()
                messages.success(request, 'Регистрация прошла успешно. Пожалуйста, войдите в свой аккаунт.')
                return redirect('success_auth')
            else:
                form.add_error('password2', "Пароли не совпадают")
    else:
        form = SignUpForm()
    return render(request, 'exam/auth.html', {'form': form})


def unauthorized(request):
    return render(request, 'exam/404.html')


class AuthProcess(View):
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('my_acc')
        else:
            return render(request, 'exam/auth.html', {'error_message': 'Неверное имя пользователя или пароль.'})

def success_auth(request):
    return render(request, 'exam/success_auth.html')


@login_required
def my_tests(request):
    # Получаем уникальные названия тестов для текущего пользователя
    test_names = Task.objects.filter(task_author=request.user).values_list('task_name', flat=True).distinct()

    # Создаем словарь для хранения информации о тестах
    test_info = []

    # Получаем информацию о тестах
    for test_name in test_names:
        # Получаем количество вопросов для каждого теста
        question_count = Task.objects.filter(task_author=request.user, task_name=test_name).count()

        # Получаем subject_id для каждого теста
        subject_id = Task.objects.filter(task_author=request.user, task_name=test_name).first().subject_id

        # Получаем название предмета по subject_id
        subject_name = Subject.objects.get(id=subject_id).subject

        # Добавляем информацию о тесте в словарь
        test_info.append({
            'test_name': test_name,
            'subject_name': subject_name,
            'question_count': question_count
        })

    return render(request, 'exam/my_tests.html', {'test_info': test_info})

def edit_test(request, task_name):
    tasks = Task.objects.filter(task_name=task_name, task_author=request.user)
    print([task.task_content for task in tasks])

    if request.method == 'POST':
        if 'apply_changes' in request.POST:
            for task in tasks:
                task_content = request.POST.get(f'task_content_{task.id}')
                correct_answer = request.POST.get(f'correct_answer_{task.id}')
                wrong_1 = request.POST.get(f'wrong_1_{task.id}')
                wrong_2 = request.POST.get(f'wrong_2_{task.id}')
                wrong_3 = request.POST.get(f'wrong_3_{task.id}')

                # Проверка на стороне сервера
                if not task_content or not correct_answer or not wrong_1 or not wrong_2 or not wrong_3:
                    # Обработка ошибки, если какое-то из обязательных полей пустое
                    return render(request, 'exam/edit_test.html', {
                        'tasks': tasks,
                        'error': 'Пожалуйста, заполните все обязательные поля.'
                    })

                task.task_content = task_content
                task.correct_answer = correct_answer
                task.wrong_1 = wrong_1
                task.wrong_2 = wrong_2
                task.wrong_3 = wrong_3
                task.task_hint = request.POST.get(f'task_hint_{task.id}')
                task.save()

        elif 'delete' in request.POST:
            tasks.delete()
            return redirect('success_auth')

        elif 'add' in request.POST:
            new_task = Task.objects.create(
                subject=tasks.first().subject,
                task_author=request.user,
                task_name=task_name,
                task_content='',
                correct_answer='',
                wrong_1='',
                wrong_2='',
                wrong_3='',
                task_hint=''
            )
            new_task.save()
            tasks = Task.objects.filter(task_name=task_name, task_author=request.user)

        for task in tasks:
            if f'delete_task_{task.id}' in request.POST:
                task.delete()
                tasks = Task.objects.filter(task_name=task_name, task_author=request.user)
                break

    return render(request, 'exam/edit_test.html', {'tasks': tasks})



def my_authors(request):
    authors = User.objects.filter(task__isnull=False).distinct()
    return render(request, 'exam/my_authors.html', {'authors': authors})

def my_acc(request):
    users = User.objects.all()
    return render(request, 'exam/my_acc.html', {'users': users})


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

def success_creation(request):
    return render(request, 'exam/success_creation.html')



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


        return redirect('success_creation')

    subjects = Subject.objects.all()
    print(subjects)
    return render(request, 'exam/create_test.html', {'subjects': subjects})


def check_task_name(request):
    task_name = request.GET.get('task_name')
    exists = Task.objects.filter(task_name=task_name).exists()
    return JsonResponse({'exists': exists})


def author_tests(request, username):
    author = get_object_or_404(User, username=username)
    grouped_tasks = Task.objects.filter(task_author=author).values('task_name').annotate(task_count=Count('id')).distinct()
    return render(request, 'exam/author_tests.html', {'author': author, 'grouped_tasks': grouped_tasks})


@login_required
def take_test(request, task_name):
    session_key = uuid.uuid4()  # Генерируем уникальный ключ для текущей сессии
    request.session['session_key'] = str(session_key)  # Сохраняем ключ в сессии

    tasks = Task.objects.filter(task_name=task_name)
    if request.method == 'POST':
        for task in tasks:
            user_response = request.POST.get(f'task_{task.id}', None)
            if user_response is None:
                user_response = ""  # Обработка случая, если пользователь не выбрал ответ

            is_correct = (user_response == task.correct_answer)
            UserAnswer.objects.create(
                user=request.user,
                task=task,
                user_response=user_response,
                is_correct=is_correct,
                timestamp=timezone.now(),
                session_key=session_key  # Сохраняем session_key для каждого ответа
            )
        return redirect('test_results', task_name=task_name)

    # Перемешивание вариантов ответов
    for task in tasks:
        options = [task.correct_answer, task.wrong_1, task.wrong_2, task.wrong_3]
        options = [opt for opt in options if opt]  # Удаление пустых вариантов
        random.shuffle(options)
        task.shuffled_options = options

    context = {
        'tasks': tasks,
        'task_name': task_name,
    }
    return render(request, 'exam/take_test.html', context)



@login_required
def test_results(request, task_name):
    session_key = request.session.get('session_key')

    if not session_key:
        # Если по какой-то причине нет ключа сессии, перенаправляем на страницу с тестами
        return redirect('take_test', task_name=task_name)

    tasks = Task.objects.filter(task_name=task_name)
    user_answers = UserAnswer.objects.filter(user=request.user, task__task_name=task_name, session_key=session_key)

    correct_count = user_answers.filter(is_correct=True).count()
    total_count = tasks.count()
    score = (correct_count / total_count) * 100 if total_count > 0 else 0

    context = {
        'task_name': task_name,
        'correct_count': correct_count,
        'total_count': total_count,
        'score': score,
        'user_answers': user_answers,
    }
    return render(request, 'exam/test_results.html', context)


@login_required
def test_statistics(request, test_name):
    user_answers = UserAnswer.objects.filter(task__task_name=test_name)

    total_attempts = user_answers.count()
    correct_attempts = user_answers.filter(is_correct=True).count()
    correct_percentage = round((correct_attempts / total_attempts) * 100, 2) if total_attempts > 0 else 0

    user_stats = user_answers.values('user__username', 'session_key').annotate(
        total=Count('id'),
        correct=Count('id', filter=Q(is_correct=True)),
        correct_percentage=ExpressionWrapper(
            Count('id', filter=Q(is_correct=True)) * 100.0 / Count('id'),
            output_field=FloatField()
        ),
        last_attempt_time=Max('timestamp')
    ).order_by('-last_attempt_time')

    context = {
        'test_name': test_name,
        'total_attempts': total_attempts,
        'correct_attempts': correct_attempts,
        'correct_percentage': correct_percentage,
        'user_stats': user_stats,
    }

    return render(request, 'exam/test_statistics.html', context)


def custom_404(request, exception):
    return render(request, '404.html', status=404)
