from django.db import models
from ..validators import validate_image_size, validate_image_format

class Story(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_email = models.EmailField()
    student_name = models.CharField(max_length=100)
    varsity_name = models.CharField(max_length=100)
    story_photo = models.ImageField(
        upload_to="./story_photos",
        blank=True,
        null=True,
        validators=[validate_image_size, validate_image_format],
    )

    def __str__(self):
        return self.student_name

