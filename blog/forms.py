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
            'parrent', 
            'parrents_phone', 
            'parrents_email',
            'phone',
            'email',
            'shirt_size'
        ]
        widgets = {
            'birth_date': DateInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit', css_class='btn btn-outline-info'))