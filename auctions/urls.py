from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_listing_page", views.create_listing, name="new_listing_page"),
    path("element/<str:id>", views.element, name="element"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:category_a>", views.select_category, name="select_category"),
    path("follow/<int:id>", views.follow, name="follow"),
    path("follow/", views.follow_list, name="follow_list"),
    path("delete/<int:id>", views.delete, name="delete"),
    path("close/<int:id>", views.close),
    path("my_listing", views.my_listings, name="my_listing"),
]
