import os
from io import BytesIO

import qrcode
from django.conf import settings
from django.core.files.base import ContentFile

from camp.models import BankAccount, SummerCampInfo


class QRPayGenerator:
    '''
    An QRPayGenerator class generates a QR code to pay for the summer camp.

    Attributes
    ----------
    ministrant : Ministrant
        A Ministrant instance
    '''
    def __init__(self, ministrant) -> None:
        self.ministrant = ministrant
        self._qr_pay_data = None
    
    def collect_qr_data(self) -> str:
        '''
        Collects data for the QR code.
        '''
        iban = BankAccount.objects.first().iban
        
        summer_camp_price = SummerCampInfo.objects.first().price
        qr_msg = self.ministrant.unicode_name
        variable_symbol = self.ministrant.variable_symbol

        return f'SPD*1.0*ACC:{iban}*AM:{summer_camp_price}*CC:CZK*MSG:{qr_msg}*X-VS:{variable_symbol}*X-KS:0308'
    
    def generate_qr_pay_code(self) -> qrcode.image:
        '''
        Generates a QR code for the ministrant.
        '''
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=1,
        )
        print(self.collect_qr_data())

        qr.add_data(self.collect_qr_data())
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        buf = BytesIO()
        img.save(buf, format='PNG')

        buf.seek(0)
        os.makedirs(os.path.join(settings.MEDIA_ROOT, 'qr_codes'), exist_ok=True)
        self.ministrant.qr_pay_code.save(f'{self.ministrant.unicode_name}.png', ContentFile(buf.getvalue()), save=True)

        return img
    
    def save_qr_pay_code(self) -> None:
        '''
        Saves the QR code to the ministrant's instance.
        '''
        img = self.generate_qr_pay_code()
        filename = f'{self.ministrant.unicode_name}.png'
        self.ministrant.qr_pay_code = os.path.join('qr_codes', filename)
        img.save(os.path.join('media', self.ministrant.qr_pay_code))