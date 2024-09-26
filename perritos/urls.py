"""
URL configuration for perritos project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from cartilla import views as cartilla_views
from sistema import views as sistema_views

urlpatterns = [
    path('admin/', admin.site.urls),
    # CUTOM URLS
    path('', cartilla_views.index, name='index'),
    path('login/', sistema_views.login_view, name='login'),
    path('logout/', sistema_views.logout_view, name='logout'),
    path('register/<str:type>', sistema_views.register_view, name='register'),
    path('register_pet/', sistema_views.register_pet, name='register_pet'),
    path('veteri/', sistema_views.veteri_view, name='veteri'),
    path('messages/', sistema_views.messages_view, name='messages'),
    path('get_messages/', sistema_views.get_message, name='get_messages'),
]
