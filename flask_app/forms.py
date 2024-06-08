# accounts/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Account

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60, help_text='Required. Add a valid email address.')

    class Meta:
        model = Account
        fields = ('email', 'password1', 'password2')
from django import forms
from .models import Recipe

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['DishName', 'DishType', 'DishSort', 'DishTime', 'ProductOtherProducts', 'Description', 'Machinery']

from django import forms

class SearchRecipeForm(forms.Form):
    word1 = forms.CharField(required=False)
    word2 = forms.CharField(required=False)
    word3 = forms.CharField(required=False)
    dishtime = forms.CharField(required=False)