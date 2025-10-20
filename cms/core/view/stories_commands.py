# CQRS
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..service.stories_commands import StoriesCommands
from ..stories_serializers import StorySerializer

class StoriesCreateView(APIView):
    @staticmethod
    def post( request):
        data = request.data
        story = StoriesCommands.create_stories(
            data['user_email'], data['student_name'], data['varsity_name'], data['story_photo']
        )
        serializer = StorySerializer(story)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class StoriesUpdateView(APIView):
    @staticmethod
    def put( request, pk):
        data = request.data
        story = StoriesCommands.update_story(
            pk, data['user_email'], data['student_name'], data['varsity_name'], data['story_photo']
        )
        serializer = StorySerializer(story)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StoriesDeleteView(APIView):
    def delete(self, request, pk=None):
        print(pk, "data")
        story = StoriesCommands.delete_story(pk)
        serializer = StorySerializer(story)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
