import os

from blog.models import Ministrant
from camp.models import SummerCampInfo, BankAccount
from ministrants_registration import settings

from utils.latex_generator import LaTeX_to_PDF_Generator


class PrintOutFormGenerator(LaTeX_to_PDF_Generator):
    def __init__(self, ministrant: Ministrant):
        super().__init__(
            template_path=os.path.join(settings.TEMPLATES[0]['DIRS'][0], 'printout_form.tex'),
            output_directory=None,
            output_filename=None,
            input_data=None
            )

        self.ministrant = ministrant

    def generate_printout_form(self):
        self.input_data = {
            'ministrant': self.ministrant,
            'summercamp': SummerCampInfo.objects.first(),
            'bank_account': BankAccount.objects.first(),
        }

        self.output_directory = rf'{settings.BASE_DIR}\media\printout_forms\{self.ministrant.unicode_name}'
        self.output_filename = f'{self.ministrant.unicode_name}.pdf'

        self.generate_pdf()

        return self.output_filename_path