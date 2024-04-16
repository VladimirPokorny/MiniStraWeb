from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
import qrcode
import os
from django.conf import settings
from io import BytesIO
from django.core.files.base import ContentFile
from unidecode import unidecode

from django.core.validators import RegexValidator
from camp.models import BankAccount, SummerCampInfo


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
    phone_regex = RegexValidator(
        regex=r'^\+(?:\d{3}\s?){4}$',
        message="Telefonní číslo musí být zadáno ve formátu: '+420 999 999 999'."
    )

    def __init__(self, *args, **kwargs) -> None:
        kwargs['max_length'] = 15
        kwargs['validators'] = [self.phone_regex]
        super().__init__(*args, **kwargs)


class Ministrant(models.Model):
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
        """
        Returns a string representation of the object containing the surname and birth name.

        :return: A string representing the object.
        """
        return f'{self.surname} {self.birthname}'

    def get_absolute_url(self) -> str:
        """
        Returns the absolute URL to access the detail view of a `Ministrant` instance.

        :param self: The `Ministrant` instance to generate the URL for.
        :type self: Ministrant
        :return: The absolute URL to access the detail view of the `Ministrant` instance.
        :rtype: str
        """
        return reverse('ministrant-detail', kwargs={'pk': self.pk})
    
    @property
    def variable_symbol(self) -> str:
        actual_camp_year = SummerCampInfo.objects.first().start_date.year
        return f'{actual_camp_year}{self.pk:04d}'

    @property
    def unicode_name(self) -> str:
        return unidecode(f'{self.surname}_{self.birthname}')


    def generate_qr_pay_code(self) -> qrcode.image:
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=1,
        )
        print(self.collect_qr_data())

        qr.add_data(self.collect_qr_data())
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        buf = BytesIO()
        img.save(buf, format='PNG')

        # Rewind the file.
        buf.seek(0)
        os.makedirs(os.path.join(settings.MEDIA_ROOT, 'qr_codes'), exist_ok=True)
        self.qr_pay_code.save(f'{self.unicode_name}.png', ContentFile(buf.getvalue()), save=True)

        return img
    
    def collect_qr_data(self) -> str:
        prefix_number = BankAccount.objects.first().number
        surfix_number = BankAccount.objects.first().bank_code
    
        account_number = f'{prefix_number}{surfix_number}' 
        
        summer_camp_price = SummerCampInfo.objects.first().price
        qr_msg = unidecode(f'{self.surname}_{self.birthname}')

        return f'SPD*1.0*ACC:{account_number}*AM:{summer_camp_price}*CC:CZK*MSG:{qr_msg}*X-VS:{self.variable_symbol}*X-KS:0308'

    
    def save(self, *args, **kwargs) -> None:
        super().save(*args, **kwargs)  # Call the "real" save() method.
        if not self.qr_pay_code:
            img = self.generate_qr_pay_code()
            filename = f'{self.unicode_name}.png'
            self.qr_pay_code = os.path.join('qr_codes', filename)
            img.save(f'media/{self.qr_pay_code}')
        return None



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
# Velikost trička	dle zákona č. 101/2000 Sb., o ochraně osobních údajů; EU 2016/67
