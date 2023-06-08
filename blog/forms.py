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
        fields = ['birthname', 'surname', 'birth_date', 'address', 'town', 'town_zip', 'insurance', 'alergy', 'swimming', 'parrent', 'parrents_phone', 'parrents_email',]
        widgets = {
            'birth_date': DateInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit', css_class='btn btn-outline-info'))


# time_stamp = models.DateTimeField(default=timezone.now)
# birthname = models.CharField(max_length=100)
# surname = models.CharField(max_length=100)
# birth_date = models.DateField()
# address = models.CharField(max_length=100)
# town = models.CharField(max_length=100)
# town_zip = models.CharField(max_length=100)

# insurance = models.CharField(max_length=3, choices=INSURANCES)

# parrent = models.CharField(max_length=100)
# parrents_phone = models.CharField(max_length=100)
# parrents_email = models.CharField(max_length=100)

# author = models.ForeignKey(User, on_delete=models.CASCADE)
