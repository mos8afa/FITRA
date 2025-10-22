from django.urls import path
from .views import register_member

app_name = 'register'

urlpatterns = [
    path('',register_member, name='register')
]