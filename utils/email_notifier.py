from django.core.mail import send_mail
from ministrants_registration import settings
from blog.models import Ministrant
from camp.models import SummerCampInfo, BankAccount
from django.template.loader import render_to_string
import unidecode
import os


class EmailNotifier:
    def __init__(self, ministrant: Ministrant):
        self.ministrant = ministrant

    def generate_email_body(self) -> str:
        email_template = os.path.join(settings.TEMPLATES[0]['DIRS'][2], 'notification_email.html')
        self.email_body = render_to_string(email_template, {
            'ministrant': self.ministrant,
            'summercamp_info': SummerCampInfo.objects.first(),
            'bank_account': BankAccount.objects.first(),
        })
        print(self.email_body)
        return self.email_body

    def send_email(self):
        pass
        # send_mail(
        #     subject='Summer Camp Registration',
        #     message=self.generate_email_body(),
        #     from_email='noreply@ministrants_registration.com',
        #     recipient_list=[self.ministrant.email],
        #     fail_silently=False,
        # )