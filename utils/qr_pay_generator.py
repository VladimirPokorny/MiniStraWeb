from camp.models import SummerCampInfo, BankAccount
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
import os
from django.conf import settings
from django.apps import apps


class QRPayGenerator:
    def __init__(self, ministrant) -> None:
        self.ministrant = ministrant
        self._qr_pay_data = None
    
    def collect_qr_data(self) -> str:
        iban = BankAccount.objects.first().iban
        
        summer_camp_price = SummerCampInfo.objects.first().price
        qr_msg = self.ministrant.unicode_name
        variable_symbol = self.ministrant.variable_symbol

        return f'SPD*1.0*ACC:{iban}*AM:{summer_camp_price}*CC:CZK*MSG:{qr_msg}*X-VS:{variable_symbol}*X-KS:0308'
    
    def generate_qr_pay_code(self) -> qrcode.image:
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

        # Rewind the file.
        buf.seek(0)
        os.makedirs(os.path.join(settings.MEDIA_ROOT, 'qr_codes'), exist_ok=True)
        self.ministrant.qr_pay_code.save(f'{self.ministrant.unicode_name}.png', ContentFile(buf.getvalue()), save=True)

        return img
    

    def save_qr_pay_code(self) -> None:
        img = self.generate_qr_pay_code()
        filename = f'{self.ministrant.unicode_name}.png'
        self.ministrant.qr_pay_code = os.path.join('qr_codes', filename)
        img.save(os.path.join('media', self.ministrant.qr_pay_code))