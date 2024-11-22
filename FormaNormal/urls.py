from django.contrib import admin
from django.urls import path
from FormaNormal.views import mainView

urlpatterns = [
    path('', mainView, name="main"),
]
