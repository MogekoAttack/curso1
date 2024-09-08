from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse

# Create your views here.
def index(request):
        # Authenticated users view their inbox
    if request.user.is_authenticated:
        return render(request, "cartilla/home.html")

    # Everyone else is prompted to sign in
    else:
        return render(request, "cartilla/index.html")