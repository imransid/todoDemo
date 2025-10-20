# from django.shortcuts import render
# from django.http import HttpResponse
# from django.views import View
#
#
# # Create your views here.
# def hello_world(request):
#     return HttpResponse("Hello, world. You're at the polls page.")


from rest_framework import viewsets
from rest_framework.response import Response

class HelloWorldViewSet(viewsets.ViewSet):
    @staticmethod
    def list(request):
        return Response({"message": "Hello, World!"})
