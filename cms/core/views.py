from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .affiliate_university_serializer import AffiliateUniversitySerializer
from .services import AffiliatedUniversityService
from rest_framework import generics
from .models import AffiliatedUniversity

class AffiliatedUniversityListCreateView(generics.ListCreateAPIView):
    """
    This view handles the listing and creating of universities.
    """
    serializer_class = AffiliateUniversitySerializer
    service = AffiliatedUniversityService()

    def get_queryset(self):
        """
        Return the list of affiliated universities.
        """
        return self.service.get_all_affiliation_university()

    def perform_create(self, serializer):
        """
        Save the new university instance created.
        """
        university_data = serializer.validated_data
        return self.service.create_affiliated_university(university_data)

class AffiliatedUniversityDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    This view handles retrieving, updating, and deleting a university.
    """
    queryset = AffiliatedUniversity.objects.all()
    serializer_class = AffiliateUniversitySerializer
    service = AffiliatedUniversityService()

    def get_object(self):
        """
        Get a specific university by ID (pk).
        """
        university_id = self.kwargs["pk"]
        university = self.service.get_affiliation_university(university_id)
        if not university:
            raise Exception("University not found")
        return university

    def perform_update(self, serializer):
        """
        Save the updated university instance.
        """
        updated_data = serializer.validated_data
        university_id = self.kwargs["pk"]
        return self.service.update_affiliation_university(university_id, updated_data)

    def perform_destroy(self, instance):
        """
        Delete a university instance.
        """
        university_id = instance.id
        return self.service.remove_affiliation_university(university_id)
