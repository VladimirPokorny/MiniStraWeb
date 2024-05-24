from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os
from ministrants_registration import settings
from django.core.files.base import ContentFile


class MinistrantImageGenerator:
    def __init__(self, ministrant):
        self.ministrant = ministrant

    def extract_initials(self):
        birthname = self.ministrant.birthname
        surname = self.ministrant.surname
        initials = birthname[0] + surname[0]
        return initials.upper()

    def generate_image(self):
        initials = self.extract_initials()
        image = Image.new('RGB', (300, 300), color=(34, 148, 210))
        draw = ImageDraw.Draw(image)

        font = ImageFont.truetype('arial.ttf', 120)
        text_width, text_height = draw.textbbox((0, 0), initials, font=font)[2:]

        text_x = (300 - text_width) / 2
        text_y = (300 - text_height) / 2

        draw.text((text_x, text_y), initials, font=font, fill='white')

        buf = BytesIO()
        image.save(buf, format='PNG')

        buf.seek(0)
        os.makedirs(os.path.join(settings.MEDIA_ROOT, 'images'), exist_ok=True)
        self.ministrant.image.save(f'{self.ministrant.unicode_name}_initials.png', ContentFile(buf.getvalue()), save=True)

        return image