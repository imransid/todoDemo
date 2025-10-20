# CQRS
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from ..model_stories import Story

class StoriesCommands():
    @staticmethod
    def create_stories(user_email, student_name, varsity_name, story_photo):
        try:
           story = Story.objects.create(
                user_email=user_email,
                student_name=student_name,
                varsity_name=varsity_name,
                story_photo=story_photo
            )
           return story
        except ValidationError as e:
            print(e)
            raise e
        except Exception as e:
            print(e)
            raise e

    @staticmethod
    def update_story(story_id, user_email=None, student_name=None, varsity_name=None, story_photo=None):

        try:
            # Get the story to update
            story = Story.objects.get(id=story_id)

            # Update fields if new values are provided
            if user_email:
                story.user_email = user_email
            if student_name:
                story.student_name = student_name
            if varsity_name:
                story.varsity_name = varsity_name
            if story_photo:
                story.story_photo = story_photo

            # Save the updated story
            story.save()
            return story
        except ObjectDoesNotExist:
            print(f"Story with ID {story_id} not found.")
            raise
        except Exception as e:
            print(f"Error updating story: {e}")
            raise

    @staticmethod
    def delete_story(story_id):
        try:
            # Get the story to delete
            story = Story.objects.get(id=story_id)
            story.delete()
        except ObjectDoesNotExist:
            print(f"Story with ID {story_id} not found.")
            raise
        except Exception as e:
            print(f"Error deleting story: {e}")
            raise



