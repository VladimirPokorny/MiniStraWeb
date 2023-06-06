from django import forms
from django.forms import ModelForm

from .models import Ministrant


class DateInput(forms.DateInput):
    input_type = 'date'


class MinistrantForm(ModelForm):
    class Meta:
        model = Ministrant
        fields = ['birthname', 'surename', 'birth_date', 'address', 'town', 'town_zip']
        widgets = {
            'birth_date': DateInput(),
        }
