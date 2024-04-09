from django.shortcuts import render, redirect
from .models import Category, UserPrompt, UserFavoriteImprovement
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm



# Create your views here.
def home(request):
    return render(request, 'home.html')

def categories(request):
    all_categories = Category.objects.all()
    return render(request, 'categories.html', {'categories': all_categories})

def prompt(request, category_id):
    prompts = UserPrompt.objects.filter(category=category_id)
    category = Category.objects.get(id=category_id)
    return render(request, 'prompt.html', {'prompts': prompts, 'category': category})

def favorites_index(request):
    if request.user.is_authenticated:
        favorites = UserFavoriteImprovement.objects.filter(user=request.user)
    else:
        favorites = None
    return render(request, 'favorites/index.html', {'favorites': favorites})

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

