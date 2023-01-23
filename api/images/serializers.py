from rest_framework import serializers

from .models import Image
from helpers import resize
from settings import IMAGES_MAX_SIZE


class ImageSerializer(serializers.ModelSerializer):
    attachment = serializers.ImageField(write_only=True)
    width = serializers.IntegerField(min_value=0)
    height = serializers.IntegerField(min_value=0)

    class Meta:
        model = Image
        read_only_fields = ["url"]
        fields = ["id", "title", "url", "width", "height", "attachment"]

    def create(self, validated_data):
        attachment = validated_data.pop("attachment")
        width = validated_data.get("width", 0)
        height = validated_data.get("height", 0)
        validated_data["url"] = resize(attachment, width=width, height=height)
        instance = super().create(validated_data)
        return instance

    def validate_attachment(self, attrs):
        self._validate_size(attrs)
        return attrs

    @staticmethod
    def _validate_content_type(attrs):
        pass

    @staticmethod
    def _validate_size(attrs):
        if attrs.size > IMAGES_MAX_SIZE:
            raise serializers.ValidationError(
                {
                    "detail": _(
                        "Files too large. Size should not exceed %d MB." % (IMAGES_MAX_SIZE / (1024 * 1024))
                    )
                }
            )


