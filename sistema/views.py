from django.db import IntegrityError
from django.shortcuts import render, HttpResponseRedirect
from django.http.response import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Veterinian
from cartilla.models import Pet

# Create your views here.

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        email = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "cartilla/login.html", {
                "message": "Invalid email and/or password."
            })
    else:
        return render(request, "cartilla/login.html")
    
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register_view(request, type):  
    if request.method == "POST":
        if type == "owner":
            username = request.POST["username"]
            email = request.POST["email"]
            password = request.POST["password"]
            confirmation = request.POST["confirmation"]
        elif type == "vet":
            id = request.POST["id"]
            username = request.POST["username"]
            email = request.POST["email"]
            password = request.POST["password"]
            confirmation = request.POST["confirmation"]
        else:
            return render(request, "cartilla/register.html", {
                "message": "Please no modify the url c:",
            })
        
       
        if password != confirmation:
            return render(request, "cartilla/register.html", {
                "message": "Passwords must match."
            })
        
        try:
            user = User.objects.create_user(username, email, password)
            user.save()

            if type == "vet":
                print("****************************")
                print(id)
                new_vet = Veterinian()
                new_vet.user = user
                new_vet.profesional_id = id
                new_vet.save()
        except IntegrityError:
            return render(request, "cartilla/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "cartilla/register.html")
    
@login_required
def register_pet(request):
    if request.method == "POST":
        try:
            new = Pet()
            new.name = request.POST["name"]
            new.kind = request.POST["kind"]
            new.owner = request.user
            new.save()
        except IntegrityError:
            return render(request, "cartilla/register_pet.html", {
                "message": "Error in register pet",
            })
        return  HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "cartilla/register_pet.html", {

        })