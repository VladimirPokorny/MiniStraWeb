from django import forms
from django.forms import ModelForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import SummerCampInfo


class DateInput(forms.DateInput):
    input_type = 'date'


class SumerCampInfoForm(ModelForm):
    class Meta:
        model = SummerCampInfo
        fields = [
            'name', 
            'start_date', 
            'end_date', 
            'price'
        ]
        labels = {
            'name': 'název',
            'start_date': 'začátek',
            'end_date': 'konec',
            'price': 'cena'
        }
        widgets = {
            'start_date': DateInput(),
            'end_date': DateInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Odeslat', css_class='btn btn-outline-info'))