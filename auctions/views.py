from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms
from .forms import ListingForm, NewListing, NewBiding
from django.contrib import messages

from .models import User, Subasta, UserAttribute

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
        if form.is_valid():
            listing = form.save()
            listing.owner = request.user
            listing.save()
            return redirect(reverse("index"), id=listing.id)
    else:
        form = ListingForm()
    return render(request, 'auctions/new_listing.html', {
        'form': form,
    })

def element(request, id):
    if UserAttribute.objects.filter(user=request.user.pk).first() is None:
        follow = False
    else:
        follow = True
    element = Subasta.objects.filter(pk=id).first()
    if request.method == 'POST':
        form = NewBiding(request.POST)
        if form.is_valid():
            campo = form.cleaned_data['new']
            if campo <= element.starting_bid:
                messages.error(request,"The new offer must be greater than the current offer")
            else:
                element.starting_bid = campo
                element.save()
    else:
        form = NewBiding()
    return render(request, 'auctions/element.html',{
        "dato": element,
        "title": element.title,
        "text": element.text,
        "bid": element.starting_bid,
        "image": element.image_url,
        "category": element.category,
        "form": form,
        "follow": follow,
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