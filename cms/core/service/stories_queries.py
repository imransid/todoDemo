from ..model_stories import Story

class StoriesQuery:
    @staticmethod
    def get_all_stories():
        return Story.objects.all()

    @staticmethod
    def get_story(story_id):
        return Story.objects.get(pk=story_id)

