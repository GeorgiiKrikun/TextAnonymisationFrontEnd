from django import forms
from django.conf import settings
    
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
#     <form action="/action_page.php">
#     <div class="mb-3 mt-3">
#       <label for="comment">Type your text to anonymise or deanonymise below:</label>
#       <textarea class="form-control" rows="5" id="comment" name="text"></textarea>
#     </div>
#     <div class="form-check form-switch">
#         <input class="form-check-input" type="checkbox" id="mySwitch" name="Anonymise" value="yes">
#         <label class="form-check-label" for="mySwitch">Deanonymise</label>
#     </div>
#     <div>
#         <button type="submit" class="btn btn-success">Go!</button>
#     </div>
# </form>
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
    anonymise = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input',
                'id': 'b_anonymise',
            }
        ),
        label='Deanonymise'
    )
