# Create your views here.
from django.shortcuts import render

def login(request):
    return render(request, 'exam/login.html')

def my_acc(request):
    return render(request, 'exam/my_acc.html')

def my_authors(request):
    return render(request, 'exam/my_authors.html')

def my_tests(request):
    return render(request, 'exam/my_tests.html')

