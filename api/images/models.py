from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


def update_name(instance, filename):
    _, extension = filename.split(".")
    return f"{instance.title}.{extension}"


class Image(models.Model):
    title = models.CharField(max_length=128, verbose_name=_("title"), unique=True)
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()
    url = models.ImageField(upload_to=update_name)
    created_at = models.DateTimeField(
        default=timezone.now, verbose_name=_("created at")
    )

    class Meta:
        verbose_name = _("image")
        verbose_name_plural = _("images")

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title
