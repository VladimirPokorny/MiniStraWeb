from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

from django.core.validators import RegexValidator


INSURANCES = [
    ('111', 'VZP'),
    ('211', 'VZP'),
]


class PhoneField(models.CharField):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{12,15}$',
        message="Phone number must be entered in the format: '+999999999999'. Up to 15 digits allowed."
    )

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 15
        kwargs['validators'] = [self.phone_regex]
        super().__init__(*args, **kwargs)


class Ministrant(models.Model):
    time_stamp = models.DateTimeField(default=timezone.now)
    birthname = models.CharField(max_length=100)
    surename = models.CharField(max_length=100)
    birth_date = models.DateField()
    address = models.CharField(max_length=100)
    town = models.CharField(max_length=100)
    town_zip = models.CharField(max_length=100)

    insurance = models.CharField(max_length=3, choices=INSURANCES)

    parrent = models.CharField(max_length=100)
    parrents_phone = PhoneField(max_length=100)
    parrents_email = models.EmailField(max_length=100, blank=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.surename + ' ' + self.birthname

    def get_absolute_url(self):
        return reverse('ministrant-detail', kwargs={'pk': self.pk})


    # zdravotní pojišťovna	
    # Trpí dítě nějakou přecitlivělostí, alergií, astmatem? Pokud ano, jakou? (popište včetně projevů a alergenů)	
    # Trpí dítě nějakou trvalou závažnou chorobou, jakou? (epilepsie, cukrovka, apod.)	
    # Užívá Vaše dítě trvale nebo v době konání tábora nějaké léky? Pokud ano, uveďte dávkování. (co, kdy, kolik)	
    # Setkalo se dítě v době dvou týdnů před začátkem tábora s nějakou infekční chorobou?	
    # Má dítě nějaké pohybové omezení? Pokud ano, jaké?	
    # Jiné sdělení (pomočování, různé druhy fóbií, činností nebo jídla, kterým se dítě vyhýbá, hyperaktivity, zvýšená náladovost, specifické rady nebo prosby):	
    # Prohlašuji, že mé dítě: 	
    # Jméno a příjmení zákonného zástupce	
    # Telefon na zákonného zástupce	
    # E - mail na zákonného zástupce	
    # E-mail účastníka - nepovinné	
    # Telefon účastníka - nepovinné	
    # Velikost trička	dle zákona č. 101/2000 Sb., o ochraně osobních údajů; EU 2016/679