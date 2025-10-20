
from django.db import models
from ..validators import validate_image_size, validate_image_format

class AffiliatedUniversity(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_email = models.EmailField(max_length=254)
    university_name = models.CharField(max_length=254)
    university_title = models.CharField(max_length=254)
    university_photo = models.ImageField(
        upload_to='university_photos/',
        blank=True,
        null=True,
        validators=[validate_image_size, validate_image_format]  # Using the custom validators here
    )

    def __str__(self):
        return self.university_name

