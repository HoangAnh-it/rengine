from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path("<slug:slug>/", views.phishing, name="phishing"),
]
