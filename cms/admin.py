from django.contrib import admin
from .core.models import AffiliatedUniversity
from .core.model_stories import Story

# Register your models here.
admin.site.register(AffiliatedUniversity)
admin.site.register(Story)
