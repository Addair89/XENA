from django.shortcuts import render


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
