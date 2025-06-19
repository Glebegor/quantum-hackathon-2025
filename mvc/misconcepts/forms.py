from django import forms

class WatsonPromptForm(forms.Form):
    topic1 = forms.CharField(label='Your Answer', max_length=200)
