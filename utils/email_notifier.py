from django.core.mail import send_mail
from ministrants_registration import settings
from blog.models import Ministrant
from camp.models import SummerCampInfo, BankAccount
from django.template.loader import render_to_string
import os
from django.core import mail


class EmailNotifier:
    def __init__(self, ministrant: Ministrant):
        self.ministrant = ministrant

    def generate_email_body(self) -> str:
        email_template = os.path.join(settings.TEMPLATES[0]['DIRS'][2], 'notification_email.html')
        self.email_body = render_to_string(email_template, {
            'ministrant': self.ministrant,
            'summercamp': SummerCampInfo.objects.first(),
            'bank_account': BankAccount.objects.first(),
        })
        return self.email_body

    def send_email(self):
        subject = 'Summer Camp Registration'
        from_email = settings.EMAIL_HOST_USER
        to = self.ministrant.parents_email
        text_content = 'This is an important message.'
        html_content = self.generate_email_body()

        email = mail.EmailMultiAlternatives(subject, text_content, from_email, [to])
        email.attach_alternative(html_content, "text/html")

        email.send()