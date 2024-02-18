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
        fields = ['birthname', 'surname', 'birth_date', 'address', 'town', 'town_zip', 'insurance', 'alergy', 'swimming', 'parent', 'parents_phone', 'parents_email',]
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
            'parents_email': 'e-mail rodiče'
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


# time_stamp = models.DateTimeField(default=timezone.now)
# birthname = models.CharField(max_length=100)
# surname = models.CharField(max_length=100)
# birth_date = models.DateField()
# address = models.CharField(max_length=100)
# town = models.CharField(max_length=100)
# town_zip = models.CharField(max_length=100)

# insurance = models.CharField(max_length=3, choices=INSURANCES)

# parent = models.CharField(max_length=100)
# parents_phone = models.CharField(max_length=100)
# parents_email = models.CharField(max_length=100)

# author = models.ForeignKey(User, on_delete=models.CASCADE)
