"""
URL configuration for exampro project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from exam.views import *
from exampro import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_page, name='main_page'),


    path('auth/', auth, name='auth'),
    path('success_auth/', success_auth, name='success_auth'),
    path('auth_process/', AuthProcess.as_view(), name='auth_process'),
    path('unauthorized/', unauthorized, name='unauthorized'),

    path('account/', my_acc, name='my_acc'),
    path('my_authors/', my_authors, name='my_authors'),
    path('my_tests/', my_tests, name='my_tests'),

    path('update_profile/', update_profile, name='update_profile'),
    path('update_avatar/', update_avatar, name='update_avatar'),

    path('create_test/', create_test, name='create_test'),
    path('success_creation/', success_creation, name='success_creation'),
    path('check_task_name/', check_task_name, name='check_task_name'),
    path('edit_test/<str:task_name>/', edit_test, name='edit_test'),

    path('<str:username>/tests/', author_tests, name='author_tests'),
    path('take_test/tests/<str:task_name>/', take_test, name='take_test'),
    path('test_results/<str:task_name>/', test_results, name='test_results'),
    path('test_statistics/<str:test_name>/', test_statistics, name='test_statistics'),


]
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
