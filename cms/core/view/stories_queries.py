from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..model_stories import Story
from ..stories_serializers import StorySerializer


class StoryListView(APIView):
    """
    API view to retrieve all stories or create a new story.
    """
    def get(self, request, *args, **kwargs):
        stories = Story.objects.all()
        serializer = StorySerializer(stories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class StoryDetailView(APIView):
    def get(self, request, pk):
        try:
            story = Story.objects.get(pk=pk)
            serializer = StorySerializer(story)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Story.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)