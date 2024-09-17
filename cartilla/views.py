from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse

from .models import Pet
from sistema.models import Veterinian

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        pets = Pet.objects.filter(owner_id=request.user.pk).all()
        user_type = Veterinian.objects.filter(user_id=request.user.pk).first()
        return render(request, "cartilla/home.html", {
            "pets": pets,
            "type": user_type,
        })
    else:
        return render(request, "cartilla/index.html")