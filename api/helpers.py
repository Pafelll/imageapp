from io import BytesIO
from PIL import Image as PIL_Image


IMAGE_CONTENT_TYPE = {
    "image/jpg": "JPEG",
    "image/jpeg": "JPEG",
    "image/png": "PNG",
    "image/gif": "GIF",
}


def resize(image_obj, width, height):
    image_file = BytesIO(image_obj.read())
    with PIL_Image.open(image_file) as image:
        image = image.resize((width, height), PIL_Image.LANCZOS)
        image_file = BytesIO()
        img_format = IMAGE_CONTENT_TYPE.get(image_obj.content_type)
        image.save(image_file, format=img_format)
        image_obj.file = image_file
    return image_obj
