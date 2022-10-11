from django.urls import path
from . import views

urlpatterns = [
    path('', views.qbe, name='qbe'),
]