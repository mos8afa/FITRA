from django.urls import path
from .views import register

app_name = 'members'

urlpatterns = [
    path('',register, name='register')
]