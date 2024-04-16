from django.template.loader import render_to_string
from ministrants_registration import settings
from blog.models import Ministrant
from camp.models import SummerCampInfo, BankAccount
from unidecode import unidecode
import subprocess
from django.http import HttpResponse
from io import BytesIO
import os


class InvoiceGenerator:
    def __init__(self, ministrant: Ministrant.objects):
        self.ministrant = ministrant

    def generate_pdf(self, pk: Ministrant.pk):
        self.ministrant = Ministrant.objects.get(pk=pk)

        input_data = {
            'ministrant': self.ministrant,
            'summercamp': SummerCampInfo.objects.first(),
            'bank_account': BankAccount.objects.first(),
        }

        self.folder_name = f'{self.ministrant.unicode_name}'
        self.folder_path = rf'{settings.BASE_DIR}\media\invoices\{self.folder_name}'
        self.latex_path = rf'{settings.BASE_DIR}\media\invoices\{self.folder_name}\{self.folder_name}_faktura.tex'
        self.output_path = rf'{settings.BASE_DIR}\media\invoices\{self.folder_name}\{self.folder_name}_faktura.pdf'

        print('\n\n\n\n\n')
        print(self.folder_name)

        directory = os.path.dirname(self.latex_path)
        os.makedirs(directory, exist_ok=True)

        latex_empty_source = os.path.join(settings.TEMPLATES[0]['DIRS'][1], 'invoice.tex')

        print('\n\n\n\n\n')
        print(latex_empty_source)

        latex_source = render_to_string(latex_empty_source, input_data)

        print(latex_source)
        
        with open(self.latex_path, 'w') as file:
            file.write(latex_source)

        print(self.latex_path)
        print(self.folder_path)

        subprocess.run(['pdflatex', self.latex_path], cwd=self.folder_path)
        clean_latex_logs(self.folder_path)

        with open(self.output_path, 'rb') as file:
            buffer = BytesIO(file.read())

        response = HttpResponse(buffer, content_type='pdf')
        response['Content-Disposition'] = 'inline; filename="ministrant.pdf"'

        return response


def clean_latex_logs(directory):
    latex_aux_files = ['.aux', '.log', '.out', '.toc']

    for filename in os.listdir(directory):
        if os.path.splitext(filename)[1] in latex_aux_files:
            os.remove(os.path.join(directory, filename))