from django.urls import path
from main.controllers import user

urlpatterns = [
       path('register', user.save, name="register"),
       path('login', user.login, name="register"),
       path('profile/<str:id>', user.profile, name="profile")]
