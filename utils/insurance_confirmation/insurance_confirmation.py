import os

from blog.models import Ministrant
from camp.models import SummerCampInfo, BankAccount
from ministrants_registration import settings

from utils.latex_generator import LaTeX_to_PDF_Generator


class InsuranceConfirmation(LaTeX_to_PDF_Generator):
    def __init__(self, ministrant: Ministrant):
        super().__init__(
            template_path=os.path.join(settings.TEMPLATES[0]['DIRS'][3], 'confirmation.tex'),
            output_directory=None,
            output_filename=None,
            input_data=None
            )

        self.ministrant = ministrant

    def generate_insurance_confirmation(self):
        insurance_confirmation_form = os.path.join(settings.STATIC_ROOT, 'utils', 'insurance_confirmation', '205_insurance_confirmation.pdf')
        print(f"Input PDF path: {insurance_confirmation_form}")

        if not os.path.exists(insurance_confirmation_form):
            raise FileNotFoundError(f"The file {insurance_confirmation_form} does not exist.")

        insurance_confirmation_form = self.convert_media_image_path_to_latex(insurance_confirmation_form)
        print(f"Converted PDF path: {insurance_confirmation_form}")

        # Define the output directory and ensure it exists
        self.output_directory = os.path.join(settings.BASE_DIR, 'media', 'insurance_confirmation', self.ministrant.unicode_name)
        os.makedirs(self.output_directory, exist_ok=True)

        # Define the output filename and path
        self.output_filename = f'{self.ministrant.unicode_name}.pdf'
        self.output_filename_path = os.path.join(self.output_directory, self.output_filename)

        self.input_data = {
            'ministrant': self.ministrant,
            'summercamp': SummerCampInfo.objects.first(),
            'bank_account': BankAccount.objects.first(),
            'insurance_confirmation_form': insurance_confirmation_form,
        }

        self.generate_pdf()

        return self.output_filename_path