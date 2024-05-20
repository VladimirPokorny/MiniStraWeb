from django.template.loader import render_to_string
import subprocess
import os
import shutil


class LaTeX_to_PDF_Generator:
    def __init__(self, template_path: str, output_directory: str, output_filename: str, input_data: dict) -> None:
        """Generates a PDF file from a LaTeX template.

        :param template_path: The path to the LaTeX template file.
        :param output_path: The path to the output folder where PDF file will be stored.
        :param file_name: The name of the output PDF file.
        :param input_data: The data to be rendered in the LaTeX template.
        """
        self.template_path = template_path
        self.output_directory = output_directory
        self.output_filename = output_filename
        self.input_data = input_data

        self.input_filename_path = None

        check_file()

    def check_output_filename_extension(self) -> None:
        check_file()

        if not self.output_filename.endswith('.pdf'):
            self.output_filename.split('.')[0] + '.pdf'

    def set_input_filename_path(self) -> None:
        check_file()
        self.input_filename_path = os.path.join(self.output_directory, self.output_filename.split('.')[0] + '.tex')

    def copy_latex_style_files(self, style_files: list) -> None:
        self.create_output_directory()
        for style_file in style_files:
            shutil.copy(style_file, self.output_directory)

    def create_output_directory(self) -> None:
        os.makedirs(self.output_directory, exist_ok=True)

    def make_tex_file(self) -> None:
        check_file()
        self.check_output_filename_extension()
        self.set_input_filename_path()

        self.output_filename_path = os.path.join(self.output_directory, self.output_filename)

        self.create_output_directory()

        print('template_path:', self.template_path)

        self.latex_source = render_to_string(self.template_path, self.input_data)

        with open(self.input_filename_path, 'w') as file:
            file.write(self.latex_source)

    def generate_pdf(self):
        check_file()
        self.make_tex_file()

        completed_process = subprocess.run(['pdflatex', self.input_filename_path], cwd=self.output_directory)

        if completed_process.returncode == 0:  # pdflatex completed successfully
            clean_latex_logs(self.output_directory)
        else:
            raise Exception(f"pdflatex process failed with return code {completed_process.returncode}")

        return self.output_filename_path


def clean_latex_logs(directory):
    latex_aux_files = ['.aux', '.log', '.out', '.toc']

    for filename in os.listdir(directory):
        if os.path.splitext(filename)[1] in latex_aux_files:
            os.remove(os.path.join(directory, filename))

def check_file(path = r'C:\Programming\MiniStraWeb\media\invoices\test_tester'):
    print("___________________________________________________________")
    if os.path.isfile(path):
        print(f"{path} is a file.")
    elif os.path.isdir(path):
        print(f"{path} is a directory.")
    else:
        print(f"{path} does not exist.")
    print("___________________________________________________________")
    print("\n\n")