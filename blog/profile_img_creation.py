from PIL import Image, ImageDraw, ImageFont


def create_profile_img(initial_letters, canvas_color, img_size):
    img = Image.new('RGB', (img_size, img_size), canvas_color)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('arial.ttf', size=img_size // 2)

    letter_width, letter_height = draw.textsize(initial_letters, font=font)
    letter_x = (img_size - letter_width) // 2
    letter_y = (img_size - letter_height) // 2
    draw.text((letter_x, letter_y), initial_letters, fill='white', font=font)

    img.save(initial_letters + '.png', 'PNG')
    return img
