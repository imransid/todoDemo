from django.urls import  path
from rest_framework import permissions
from .core.views import AffiliatedUniversityAPIView
from .core.view.stories_commands import StoriesCreateView, StoriesUpdateView, StoriesDeleteView
from .core.view.stories_queries import StoryListView, StoryDetailView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


# Define the schema view for the documentation
schema_view = get_schema_view(
   openapi.Info(
      title="My API",
      default_version='v1',
      description="API documentation for my Django project",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@myapi.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   urlconf='cms.urls',
   permission_classes=(permissions.AllowAny,),  # Correct format: tuple with a single class
)


urlpatterns = [
    # path('affiliated_universities/', AffiliatedUniversityAPIView.as_view(), name='affiliated_university'),
    # path('affiliated_universities/<int:pk>/', AffiliatedUniversityAPIView.as_view(), name='affiliated_university_detail'),

# query
    path('stories/', StoryListView.as_view(), name='stories_list'),
    path('stories/<int:pk>/', StoryDetailView.as_view(), name='story_detail'),

# command
    path('stories/create', StoriesCreateView.as_view(), name='stories_create'),
    path('stories/update/<int:pk>/', StoriesUpdateView.as_view(), name='stories_update'),
    path('stories/delete/<int:pk>/', StoriesDeleteView.as_view(), name='stories_delete'),

# your existing API endpoints
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-docs'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc-docs'),
]

