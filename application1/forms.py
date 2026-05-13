from django import forms
from application1.models import login
class LoginForm(forms.ModelForm):
    username=forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder':'Username'
            }
        )
    )
    password=forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder':'Password'
            }
        )
    )
    class Meta:
        model=login
        fields="__all__"