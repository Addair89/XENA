from django.urls import path
from . import views

urlpatterns =[
    path('', views.home, name='home'),
    path('categories/', views.categories, name='categories'),
    path('categories/<int:category_id>', views.category_detail, name='category_detail'),
    path('prompt/', views.prompt, name='prompt'),
    path('favorites/', views.favorites_index, name='favorites_index'),
    path('accounts/signup/', views.signup, name='signup'),
    path('openai/', views.openai_view, name='openai'),
    # path('prompt/<int:prompt_id>/favorite/', views.favorites_index, name='favorites_index')
]