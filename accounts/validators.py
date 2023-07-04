from rest_framework.validators import ValidationError


def validate_image_size(file_obj):
    if file_obj.size > 5000000:
        raise ValidationError("File exceeds Size limit")