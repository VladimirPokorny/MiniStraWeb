from django import forms
from django.forms import ModelForm

from .models import Ministrant


class DateInput(forms.DateInput):
    input_type = 'date'


class MinistrantForm(ModelForm):
    class Meta:
        model = Ministrant
        fields = ['birthname', 'surename', 'birth_date', 'address', 'town', 'town_zip', 'insurance', 'parrent', 'parrents_phone', 'parrents_email']
        # fields = ['parrents_phone', 'parrents_email']
        widgets = {
            'birth_date': DateInput(),
        }


    # time_stamp = models.DateTimeField(default=timezone.now)
    # birthname = models.CharField(max_length=100)
    # surename = models.CharField(max_length=100)
    # birth_date = models.DateField()
    # address = models.CharField(max_length=100)
    # town = models.CharField(max_length=100)
    # town_zip = models.CharField(max_length=100)

    # insurance = models.CharField(max_length=3, choices=INSURANCES)

    # parrent = models.CharField(max_length=100)
    # parrents_phone = models.CharField(max_length=100)
    # parrents_email = models.CharField(max_length=100)

    # author = models.ForeignKey(User, on_delete=models.CASCADE)