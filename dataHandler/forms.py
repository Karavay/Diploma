from django import forms
from django.core import validators

class DataForm(forms.Form):
    amountOfUsers = forms.IntegerField(label='amountOfUsers',max_value=100,min_value=1)
