import base64

from django.core.files.base import ContentFile
from rest_framework import serializers


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            extension, img_code = data.split(';base64,')
            extension = extension.split('/')[-1]
            data = ContentFile(base64.b64decode(img_code),
                               name=f'img.{extension}')
        return super().to_internal_value(data)
