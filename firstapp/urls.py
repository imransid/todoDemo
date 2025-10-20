from django.urls import  path
from . import views

urlpatterns = [
    path('func', views.hello_world),
    path('class/', views.HelloView.as_view(), name='class'),
    path('reservation', views.home),
]