from django.shortcuts import get_object_or_404,render, redirect
from .models import Category, UserPrompt, UserFavoriteImprovement, PromptImprovement
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .forms import OpenAIForm
from openai import OpenAI
import os


# Create your views here.
import os
from django.shortcuts import render
from .forms import OpenAIForm
from openai import OpenAI

def home(request):
    form = OpenAIForm(request.POST or None)
    response = None
    prompt_text = None
    categories = Category.objects.all()

    if request.method == 'POST':
        if form.is_valid():
            input_text = form.cleaned_data['input_text']
            prompt_text = input_text 

            API_KEY = os.getenv('API_KEY')
            client = OpenAI(api_key=API_KEY)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": input_text}]
            )
            response = response.choices[0].message.content

    return render(request, 'home.html',{'form': form, 'response': response, "categories": categories})

def categories(request):
    all_categories = Category.objects.all()
    return render(request, 'categories/index.html', {'categories': all_categories})

def prompt(request):
    prompts = UserPrompt.objects.filter(user=request.user)
    return render(request, 'prompts/index.html', {'prompts': prompts})

def add_to_favorites(request, improvement_id):
    # Get the current user and the improvement instance
    user = request.user
    improvement = get_object_or_404(PromptImprovement, id=improvement_id)

    # Get or create a UserFavoriteImprovement instance for the user
    user_favorite, created = UserFavoriteImprovement.objects.get_or_create(user=user)

    # Add the improvement to the user's favorites
    user_favorite.improvements.add(improvement)
    user_favorite.save()
    favorites = UserFavoriteImprovement.objects.filter(user=request.user).prefetch_related('improvements')

    # Flatten out the improvements into a list
    favorite_improvements = [fav.improvements.all() for fav in favorites]
    return render(request, 'prompts/favorites.html', {'favorite_improvements': favorite_improvements})


def favorites_index(request):
    if request.user.is_authenticated:
        favorites = UserFavoriteImprovement.objects.filter(user=request.user).prefetch_related('improvements')

    # Flatten out the improvements into a list
        favorite_improvements = [fav.improvements.all() for fav in favorites]
    else:
        favorites = None
    return render(request, 'prompts/favorites.html', {'favorite_improvements': favorite_improvements})

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

def category_detail(request, category_id):
    category = Category.objects.get(id=category_id)
    form = OpenAIForm(request.POST or None)
    response = None
    improved_response = None 
    user_prompt = None 
    prompt_improvement = None 
    if request.method == 'POST':
        if form.is_valid():
            input_text = form.cleaned_data['input_text']
            improvement = f'Only respond with an improved prompt, no yapping: {input_text}'
            # Send input to OpenAI API and receive response
            API_KEY = os.getenv('API_KEY')
            client = OpenAI(api_key=API_KEY)
            response = client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": input_text}])
            improved_response = client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": improvement}])
            response = response.choices[0].message.content
            improved_response = improved_response.choices[0].message.content
            user_prompt = UserPrompt(
                user=request.user,
                category=category,
                prompt=input_text
            )
            user_prompt.save()

            prompt_improvement = PromptImprovement(
                improvement=improved_response,
                user_prompt=user_prompt 
            )
            prompt_improvement.save()
    return render(request, 'categories/detail.html', 
                  {"category": category, 
                   "form": form, 
                   "response": response, 
                   "improved_response": improved_response,
                   "user_prompt": user_prompt,
                   "prompt_improvement": prompt_improvement 
                   })

























