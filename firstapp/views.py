from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from  .forms import ReservationForm


# Create your views here.
def hello_world(request):
    return HttpResponse("Hello, world. You're at the polls page.")

class HelloView(View):
    def get(self, request):
        return HttpResponse("Hello, world. You're at the polls page. Rafa")

def home(request):

    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("Successfully saved")

    return render(request, "index.html", {"form": ReservationForm()})