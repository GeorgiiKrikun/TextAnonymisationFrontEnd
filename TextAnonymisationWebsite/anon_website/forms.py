from django import forms
from TextAnonymisationEngine.Engine.Lang import Lang
    
class LoginForm(forms.Form):
    username = forms.CharField(max_length=20, 
                               widget=forms.TextInput(
                                attrs={'class': 'form-control', 'placeholder': 'Username'}
                               ))
    password = forms.CharField(max_length=64, widget=forms.PasswordInput(
                                attrs={'class': 'form-control', 'placeholder': 'Password'}
                               ))
    
class SignupForm(forms.Form):
    username = forms.CharField(max_length=20, 
                               widget=forms.TextInput(
                                attrs={'class': 'form-control', 'placeholder': 'Username'}
                               ))
    email = forms.EmailField(max_length=64, 
                                widget=forms.EmailInput(
                                    attrs={'class': 'form-control', 'placeholder': 'Email'}
                             ))
    password = forms.CharField(max_length=64, widget=forms.PasswordInput(
                                attrs={'class': 'form-control', 'placeholder': 'Password'}
                               ))
    password_confirm = forms.CharField(max_length=64, widget=forms.PasswordInput(
                                attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}
                               ))

class TryForm(forms.Form):
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 5,
                'id': 'comment',
                'placeholder': 'Type your text to anonymise or deanonymise'
            }
        ),
        label='Type your text to anonymise or deanonymise below:'
    )
    language = forms.ChoiceField(
        choices=[(lang.value, lang.name) for lang in Lang],
        widget=forms.Select(
            attrs={
                'class': 'form-select',
                'id': 'language',
            }
        ),
        label='Language'
    )
    anonymise = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input',
                'id': 'b_anonymise',
            }
        ),
        label='Deanonymise',
    )
