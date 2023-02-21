from django.contrib import admin
from django.urls import path

from authentication.views import *

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_, name='login'),
    path('logout/',logout_,name='logout'),
    path('my_profile',my_profile,name='my_profile'),
    path('change_profile/',change_profile,name='change_profile'),
    path('api/v1/user/',CustomUserApiView.as_view()),
    path('api/v1/user/<int:pk>',TheCustomUserApiView.as_view())
]

