from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class UserPrompt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    prompt = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('prompts/index.html', kwargs={'user_id': self.user.id})

class PromptImprovement(models.Model):
    improvement = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user_prompt = models.ForeignKey(UserPrompt, on_delete=models.CASCADE, related_name='improvements')

class UserFavoriteImprovement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    improvements = models.ManyToManyField(PromptImprovement)

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
class ExamplePrompt(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    text = models.TextField()    
