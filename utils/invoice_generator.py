import os

from blog.models import Ministrant
from camp.models import SummerCampInfo, BankAccount
from ministrants_registration import settings

from utils.latex_generator import LaTeX_to_PDF_Generator


class InvoiceGenerator(LaTeX_to_PDF_Generator):
    def __init__(self, ministrant: Ministrant):
        super().__init__(
            template_path=os.path.join(settings.TEMPLATES[0]['DIRS'][1], 'invoice.tex'),
            output_directory=None,
            output_filename=None,
            input_data=None
            )

        self.ministrant = ministrant

    def generate_invoice(self):
        self.input_data = {
            'ministrant': self.ministrant,
            'summercamp': SummerCampInfo.objects.first(),
            'bank_account': BankAccount.objects.first(),
            'qr_code_path': self.convert_media_image_path_to_latex(self.ministrant.qr_pay_code.url),
        }

        self.output_directory = rf'{settings.BASE_DIR}\media\invoices\{self.ministrant.unicode_name}'
        self.output_filename = f'{self.ministrant.unicode_name}_faktura.pdf'

        self.copy_latex_style_files([os.path.join(settings.TEMPLATES[0]['DIRS'][1], 'ministrant_invoice.sty')])

        self.generate_pdf()

        return self.output_filename_path
