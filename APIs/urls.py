from django.urls import path
from .views import get_member_info, EmailTokenObtainPairView, add_user

app_name = 'apis'

urlpatterns = [
    path('get_member_info/', get_member_info, name='member_info'),
    path("login/", EmailTokenObtainPairView.as_view()),
    path("signup/", add_user, name='signup'),
]