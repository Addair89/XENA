from django import forms

class OpenAIForm(forms.Form):
    input_text = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Enter prompt...'}))