from django.contrib import admin
from .models import UserPrompt, PromptImprovement, UserFavoriteImprovement, Category, ExamplePrompt

admin.site.register(UserPrompt)
admin.site.register(PromptImprovement)
admin.site.register(UserFavoriteImprovement)
admin.site.register(Category)
admin.site.register(ExamplePrompt)
