import factory

from images.models import Image


class ImageFactory(factory.django.DjangoModelFactory):
    title = factory.Sequence(lambda n: "title %d.jpg" % n)
    height = factory.Faker("pyint", min_value=100, max_value=1000)
    width = factory.Faker("pyint", min_value=100, max_value=1000)
    url = factory.django.ImageField(height=height, width=width, filename=title)

    class Meta:
        model = Image
