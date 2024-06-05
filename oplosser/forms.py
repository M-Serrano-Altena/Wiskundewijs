from django import forms

class EquationForm(forms.Form):
    equation_text = forms.CharField(
        label='Vul hier de vergelijking in',
        max_length=255,
        widget=forms.TextInput(attrs={
            'placeholder': 'bijv. 2x^2 + 1 = 9',
            'class': 'form-control'
        })
    )