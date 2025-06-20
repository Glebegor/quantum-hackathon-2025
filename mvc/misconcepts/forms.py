from django import forms

class WatsonPromptForm(forms.Form):
    topic1 = forms.CharField(
        max_length=200,
        widget=forms.Textarea(attrs={'class': 'id_topic1'}),
        label=''
    )
