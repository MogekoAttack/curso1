import json

from django.db import IntegrityError
from django.shortcuts import render, HttpResponseRedirect
from django.http.response import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Veterinian
from cartilla.models import Pet, Messages

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
    
def veteri_view(request):
    all_users = User.objects.all()
    all_vet = Veterinian.objects.all()
    vet = []
    for v in all_vet:
        for u in all_users:
            if u.pk == v.pk:
                vet.append(u)
    
    return render(request, "cartilla/veteri.html", {
        "vet": vet,
    })

def messages_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        receiver = data.get('receiver')
        body = data.get('messageBody')

        user = User.objects.filter(username=receiver).first()

        print(request.user)
        
        if user == None:
            return JsonResponse({'status': 'User not exist'}, status=200)
        
        try:
            new_message = Messages()
            new_message.sender = request.user
            new_message.receiver = user
            new_message.body = body
            new_message.save()
        except:
            return JsonResponse({'status': 'error'})
        
        return JsonResponse({'status': 'success'})
    
    messages = Messages.objects.all()
    print( len(messages))
    if len(messages) < 1:
        messages = "None"
    return render(request, 'cartilla/messages.html', {
        "messages": messages,
    })

def get_message(request):
    if request.method != 'GET':
        return JsonResponse({
            "status": "ERROR",
            "sender": "",
            "receiver": "",
            "body": "",
        })
    
    message_id = request.GET.get('id')
    message = Messages.objects.filter(receiver=request.user.pk, pk=message_id).first()
    
    if message == None:
        return JsonResponse({
            "status": "ERROR",
            "sender": "",
            "receiver": "",
            "body": "THIS MESSAGE NOT EXIST!",
        })

    return JsonResponse({
        "status": "success",
        "sender": str(message.sender),
        "receiver": str(message.receiver),
        "body": str(message.body),
    })