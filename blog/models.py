from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


class Ministrant(models.Model):
    time_stamp = models.DateTimeField(default=timezone.now)
    birthname = models.CharField(max_length=100)
    surename = models.CharField(max_length=100)
    birth_date = models.DateField()
    address = models.CharField(max_length=100)
    town = models.CharField(max_length=100)
    town_zip = models.CharField(max_length=100)

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.birthname + ' ' + self.surename

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