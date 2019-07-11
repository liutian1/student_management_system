"""day65 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from app import view

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r"^classes/",view.classes),
    url(r"^add_class/",view.add_class),
    url(r"^del_class/",view.del_class),
    url(r"^del_student/",view.del_student),
    url(r"^edit_class/",view.edit_class),
    url(r"^edit_student/",view.edit_student),
    url(r"^students/",view.students),
    url(r"^add_student/",view.add_student),
    url(r"^modal_add_class/",view.modal_add_class),
    url(r"^modal_edit_class/",view.modal_edit_class),
    url(r"^model_add_student/",view.model_add_student),
    url(r"^modal_edit_student/",view.modal_edit_student),
    url(r"^teachers/",view.teachers),
    url(r"^add_teacher/",view.add_teacher),
    url(r"^edit_teacher/",view.edit_teacher),
    url(r"^get_all_class/",view.get_all_class),
    url(r"^test/",view.test),
    url(r"^layout/",view.layout),
]
