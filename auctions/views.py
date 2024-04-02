from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms
from .forms import ListingForm, NewListing, NewBiding, Comentary
from django.contrib import messages

from .models import User, Subasta, UserAttribute, Oferta, Comentario

def index(request):
    datos = Subasta.objects.all()
    return render(request, "auctions/index.html", {
        'datos': datos,
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def new_listing_page(request):
    form = NewListing(request.POST)
    return render(request, "auctions/new_listing.html",{
        "form": NewListing(),
    })

def create_listing(request):
    if request.method == 'POST':
        form = ListingForm(request.POST)
        # print(form)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.author = request.user
            listing.open = True
            if listing.category == "":
                listing.category = "Without category"
            if listing.image_url == "":
                listing.image_url = "https://cdn-icons-png.flaticon.com/512/1257/1257249.png"
            listing.save()
            return redirect(reverse("index"), id=listing.id)
    else:
        form = ListingForm()
    return render(request, 'auctions/new_listing.html', {
        'form': form,
    })

def element(request, id):
    if UserAttribute.objects.filter(user=request.user.pk, follow_list=id).first() is None:
        follow = False
    else:
        follow = True
    element = Subasta.objects.filter(pk=id).first()
    best_bid = Oferta.objects.filter(subasta=id).last()
    if request.user == element.author:
        creator = True
    else:
        creator = False
    if request.method == 'POST':
        form = NewBiding(request.POST)
        comentario = Comentary(request.POST)
        if form.is_valid():
            campo = form.cleaned_data['new']
            if best_bid == None:
                best_bid = Oferta()
                best_bid.subasta = element
                best_bid.author = request.user
                best_bid.bid = element.starting_bid
                best_bid.save()
            if campo <= best_bid.bid:
                messages.error(request,"The new offer must be greater than the current offer")
            else:
                nueva = Oferta()
                nueva.subasta = element
                nueva.author = request.user
                nueva.bid = campo
                # element.starting_bid = campo
                nueva.save()
                # element.save()
                return HttpResponseRedirect(f"/element/{id}")
        if comentario.is_valid():
            user_text = comentario.cleaned_data['text']
            nuevo_comentario = Comentario()
            nuevo_comentario.author = request.user
            nuevo_comentario.text = user_text
            nuevo_comentario.subasta = Subasta.objects.filter(pk=id).first()
            nuevo_comentario.save()
            return HttpResponseRedirect(f"/element/{id}")
    else:
        form = NewBiding()
        comentario = Comentary()
    come = Comentario.objects.filter(subasta=id).all()
    return render(request, 'auctions/element.html',{
        "dato": element,
        "title": element.title,
        "text": element.text,
        "bid": element.starting_bid,
        "image": element.image_url,
        "category": element.category,
        "form": form,
        "follow": follow,
        "creator": creator,
        "best_bid": best_bid,
        "comentario": comentario,
        "listacomentarios": come,
    })

def categories(request):
    list = []
    list_categories = Subasta.objects.all()
    for element in list_categories:
        if not element.category in list:
            list.append(element.category)
    return render(request, 'auctions/categories.html',{
        "list": list,
    })

def select_category(request, category_a):
    list = Subasta.objects.filter(category=str(category_a)).all()
    return render(request, 'auctions/category.html',{
        "category": category_a,
        "list": list,
    })

def follow(request, id):
    dato = Subasta.objects.filter(pk=id).first()
    insert = UserAttribute()
    # print(f"{request.user}")
    if UserAttribute.objects.filter(user=request.user, follow_list=id).first():
        UserAttribute.objects.filter(user=request.user, follow_list=id).first().delete()
    else:
        insert.user = User.objects.filter(username=request.user).first()
        insert.follow_list = dato.pk
        insert.save()
    return element(request, id)

def follow_list(request):
    dato = UserAttribute.objects.filter(user=request.user).all()
    listing = []
    for pos in dato:
        listing.append(Subasta.objects.filter(pk=pos.follow_list).first())
    return render(request, 'auctions/follow_list.html',{
        "list": listing,
    })

def delete(request, id):
    # print(id)
    Subasta.objects.filter(pk=id).first().delete()
    return HttpResponseRedirect(reverse("index"))

def my_listings(request):
    winner = []
    datos = Subasta.objects.filter(author=request.user).all()
    datos_2 = Subasta.objects.filter(open=False).all()
    for dato in datos_2:
        bids = Oferta.objects.filter(subasta=dato.pk).last()
        print(f"{bids.subasta.title}")
        winner.append(bids)
            
    return render(request, 'auctions/my_listings.html',{
        "datos": datos,
        "winner": winner,
    })

def close(request, id):
    dato = Subasta.objects.filter(pk=id).first()
    dato.open = False
    dato.save()
    return HttpResponseRedirect(f"/element/{id}")
