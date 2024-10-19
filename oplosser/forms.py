from django import forms

class EquationForm(forms.Form):
    equation_text = forms.CharField(
        label='Vul hier de vergelijking in',
        max_length=255,
        widget=forms.TextInput(attrs={
            'placeholder': 'bijv. 2x^2 + 1 = 9',
            'class': 'form-control',
            'autocapitalize': 'none'
        })
    )

class QuestionForm(forms.Form):
    question = forms.CharField(
        label='Vul hier je vraag in',
        max_length=255,
        widget=forms.TextInput(attrs={
            'placeholder': 'bijv. Waarom geeft x^2 = 1 twee oplossingen?',
            'class': 'form-control'
        }),
        required=True
    )