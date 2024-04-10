from django import forms

class OpenAIForm(forms.Form):
    input_text = forms.CharField(label='Input Text', widget=forms.Textarea)