from django.db import models
from django.utils import timezone


def update_name(instance, filename):
    extension = filename.split(".")[-1]
    title = instance.title.split(".")[0]
    return f"{title}.{extension}"


class Image(models.Model):
    title = models.CharField(max_length=128, verbose_name="title", unique=True)
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()
    url = models.ImageField(upload_to=update_name)
    created_at = models.DateTimeField(default=timezone.now, verbose_name="created at")

    class Meta:
        verbose_name = "image"
        verbose_name_plural = "images"

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title
