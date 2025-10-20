from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .affiliate_university_serializer import AffiliateUniversitySerializer
from .services import AffiliatedUniversityService
class AffiliatedUniversityAPIView(APIView):
    services = AffiliatedUniversityService()

    def get(self, request, pk=None):
        id_query = request.query_params.get('id', None)
        print("Search Query:", id_query)
        """Retrieve a list of universities or a single university."""
        try:
            if pk is not None and isinstance(pk, int):  # Ensure pk is an integer
                affiliation_university = self.services.get_affiliation_university(pk)
                serializer = AffiliateUniversitySerializer(affiliation_university)
                return Response(serializer.data)
            affiliation_universities = self.services.get_all_affiliation_university()
            serializer = AffiliateUniversitySerializer(affiliation_universities, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": f"University not found: {e}"}, status=404)

    def post(self, request):
        """Create a new university."""
        serializer = AffiliateUniversitySerializer(data=request.data)
        if serializer.is_valid():
            university_data = serializer.validated_data
            affiliation_university = self.services.create_affiliated_university(university_data)
            affiliation_university_serializer = AffiliateUniversitySerializer(affiliation_university)
            return Response(affiliation_university_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        """Update an existing university."""
        updated_data = request.data
        affiliation_university = self.services.update_affiliation_university(pk, updated_data)
        serializer = AffiliateUniversitySerializer(affiliation_university)
        return Response(serializer.data)

    def delete(self, pk=None):
        """Delete an existing university."""
        self.services.remove_affiliation_university(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

