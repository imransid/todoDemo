from django.core.exceptions import ValidationError

def validate_image_size(image, max_size_mb=1):
    max_size = max_size_mb * 1024 * 1024  # Convert MB to bytes
    if image.size > max_size:
        raise ValidationError(f"Image size must be under {max_size_mb}MB.")

def validate_image_format(image):
    allowed_formats = ['image/jpeg', 'image/png', 'image/gif']
    if image.file.content_type not in allowed_formats:
        raise ValidationError("Only JPG, PNG, and GIF formats are allowed.")