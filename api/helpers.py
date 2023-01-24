from io import BytesIO
from PIL import Image as PIL_Image

ALLOWED_IMAGE_FORMAT = ["GIF", "PNG", "JPEG", "BMP"]


def resize(image_obj, width, height):
    image_file = BytesIO(image_obj.read())
    with PIL_Image.open(image_file).convert("RGB") as image:
        image = image.resize((width, height), PIL_Image.LANCZOS)
        image_file = BytesIO()
        img_format = image_obj.name.split(".")[-1]
        image.save(image_file, format=img_format)
        image_obj.file = image_file
    return image_obj
