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
    path('registration/', registration, name='registration'),
    path('my_acc/', my_acc, name='my_acc'),
    path('my_authors/', my_authors, name='my_authors'),
    path('my_tests/', my_tests, name='my_tests'),
    path('success_login/', success_login, name='success_login'),

    path('forgot_pass/', forgot_pass, name='forgot_pass'),
    path('pass_reset/', pass_reset, name='pass_reset'),
    path('code/', code, name='code'),
    path('my_login/', LoginView.as_view(), name='my_login'),
    path('update_profile/', update_profile, name='update_profile'),
    path('update_avatar/', update_avatar, name='update_avatar'),
    path('create_test/', create_test, name='create_test'),
    path('check_task_name/', check_task_name, name='check_task_name'),
]
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
