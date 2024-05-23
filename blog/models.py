import os

from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone

from unidecode import unidecode

from camp.models import SummerCampInfo
from utils.qr_pay_generator import QRPayGenerator


INSURANCE_COMPANIES = [
    ('111', '111: VZP'),
    ('201', '201: Vojenská zdravotní pojišťovna České republiky'),
    ('205', '205: Česká průmyslová zdravotní pojišťovna'),
    ('207', '207: Oborová zdravotní pojišťovna zaměstnanců bank, pojišťoven a stavebnictví'),
    ('209', '209: Zaměstnanecká pojišťovna Škoda'),
    ('211', '211: Zdravotní pojišťovna ministerstva vnitra České republiky'),
    ('213', '213: RBP, zdravotní pojišťovna'),
]


class PhoneField(models.CharField):
    '''
    A PhoneField class is a custom model field for phone numbers.
    '''
    phone_regex = RegexValidator(
        regex=r'^\+(?:\d{3}\s?){4}$',
        message="Telefonní číslo musí být zadáno ve formátu: '+420 999 999 999'."
    )

    def __init__(self, *args, **kwargs) -> None:
        kwargs['max_length'] = 15
        kwargs['validators'] = [self.phone_regex]
        super().__init__(*args, **kwargs)


class Ministrant(models.Model):
    '''
    A Ministrant class represents a person who is going to attend the summer camp.
    '''
    time_stamp = models.DateTimeField(default=timezone.now)
    birthname = models.CharField(max_length=100, blank=True)
    surname = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(blank=True)
    address = models.CharField(max_length=100, blank=True)
    town = models.CharField(max_length=100, blank=True)
    town_zip = models.CharField(max_length=100, blank=True)

    insurance = models.CharField(max_length=3, choices=INSURANCE_COMPANIES)
    alergy = models.TextField(max_length=1000, blank=True)
    swimming = models.BooleanField(default=False)

    parent = models.CharField(max_length=100, blank=True)
    parents_phone = PhoneField(max_length=100, blank=True)
    parents_email = models.EmailField(max_length=100, blank=True)

    phone = PhoneField(max_length=100, blank=True)
    email = models.EmailField(max_length=100, blank=True)
    shirt_size = models.CharField(max_length=100, blank=True)

    variable_symbol = models.CharField(max_length=100, blank=True)
    paid = models.BooleanField(default=False)

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    qr_pay_code = models.ImageField(upload_to='qr_codes', blank=True, null=True)
    unicode_name = models.CharField(max_length=100, blank=False)

    def __str__(self) -> str:
        return f'{self.surname} {self.birthname}'

    def get_absolute_url(self) -> str:
        '''
        Returns the absolute URL of the object.

        Returns
        -------
        str
            The absolute URL of the object.
        '''
        return reverse('ministrant-detail', kwargs={'pk': self.pk})

    @property
    def variable_symbol(self) -> str:
        '''
        Returns a variable symbol for the payment.

        Returns
        -------
        str
            A variable symbol for the payment.
        '''
        actual_camp_year = SummerCampInfo.objects.first().start_date.year
        return f'{actual_camp_year}{self.pk:04d}'

    @property
    def unicode_name(self) -> str:
        '''
        Returns the name of the object in a unicode format.

        Returns
        -------
        str
            The name of the object in a unicode format.
        '''
        return unidecode(f'{self.surname}_{self.birthname}')

    def save(self, *args, **kwargs) -> None:
        '''
        Saves the object to the database.
        '''
        super().save(*args, **kwargs)  # Call the "real" save() method.

        if not self.qr_pay_code:
            img = QRPayGenerator(self).generate_qr_pay_code()
            filename = f'{self.unicode_name}.png'
            self.qr_pay_code = os.path.join('qr_codes', filename)
            img.save(f'media/{self.qr_pay_code}')

            super().save(*args, **kwargs)  # Call the "real" save() method.

        return None
