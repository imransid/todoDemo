from rest_framework import serializers
from .models import AffiliatedUniversity

class AffiliateUniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = AffiliatedUniversity
        fields = ['id', 'created_at', 'updated_at', 'user_email', 'university_name', 'university_title', 'university_photo']
