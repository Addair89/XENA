from django.urls import path
from . import views

urlpatterns =[
    path('', views.home, name='home'),
    path('categories/', views.categories, name='categories'),
    path('prompt/', views.prompt, name='prompt'),
    path('favorites/', views.favorites_index, name='favorites_index'),
    path('accounts/signup/', views.signup, name='signup'),
]