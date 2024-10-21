from django.contrib import admin
from django.urls import include, path, re_path

from . import views

urlpatterns = [
    path("<slug:slug>/", views.list_targets, name="scanner_master_list_target"),
    path("<slug:slug>/<int:id>/", views.detail_target, name="scanner_master_detail_target"),
]
