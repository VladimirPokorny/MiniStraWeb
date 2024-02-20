from django import forms
from django.forms import ModelForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Ministrant


class DateInput(forms.DateInput):
    input_type = 'date'


class MinistrantForm(ModelForm):
    class Meta:
        model = Ministrant
        fields = [
            'birthname', 
            'surname', 
            'birth_date', 
            'address', 
            'town', 
            'town_zip', 
            'insurance', 
            'alergy', 
            'swimming', 
            'parent', 
            'parents_phone', 
            'parents_email',
            'phone',
            'email',
            'shirt_size'
        ]
        labels = {
            'birthname': 'jméno',
            'surname': 'příjmení',
            'birth_date': 'datum narození',
            'address': 'adresa',
            'town': 'obec',
            'town_zip': 'PSČ',
            'insurance': 'pojišťovna',
            'alergy': 'alergie',
            'swimming': 'plavec',
            'parent': 'rodič',
            'parents_phone': 'telefonní číslo rodiče',
            'parents_email': 'e-mail rodiče',
            'phone': 'telefonní číslo účastníka',
            'email': 'e-mail účastníka',
            'shirt_size': 'velikost trička'
        }
        widgets = {
            'birth_date': DateInput(),
            'insurance': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Odeslat', css_class='btn btn-outline-info'))
