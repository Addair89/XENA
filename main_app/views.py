from django.shortcuts import render, redirect
from .models import Category, UserPrompt, UserFavoriteImprovement
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .forms import OpenAIForm
from openai import OpenAI
import os



# Create your views here.
def home(request):
    return render(request, 'home.html')

def categories(request):
    all_categories = Category.objects.all()
    return render(request, 'categories/index.html', {'categories': all_categories})

def prompt(request):
    prompts = UserPrompt.objects.filter(user=request.user)
    return render(request, 'prompts/index.html', {'prompts': prompts})

def favorites_index(request):
    if request.user.is_authenticated:
        favorites = UserFavoriteImprovement.objects.filter(user=request.user)
    else:
        favorites = None
    return render(request, 'prompts/favorites.html', {'favorites': favorites})

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('home')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)


def openai_view(request):
    form = OpenAIForm(request.POST or None)
    response = None

    if request.method == 'POST':
        if form.is_valid():
            input_text = form.cleaned_data['input_text']

            # Send input to OpenAI API and receive response
            API_KEY = os.getenv('API_KEY')
            client = OpenAI(api_key=API_KEY)
            response = client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": input_text}])
            
            response = response.choices[0].message.content

    return render(request, 'openai.html', {'form': form, 'response': response})
