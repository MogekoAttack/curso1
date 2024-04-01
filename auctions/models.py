from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class UserAttribute(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    follow_list = models.CharField(
        max_length=1024,
    )

class Subasta(models.Model):
    title = models.CharField(
        max_length = 64,
    )
    text = models.CharField(
        max_length = 64,
    )
    starting_bid = models.IntegerField(
        
    )
    image_url = models.CharField(
        max_length = 1024,
    )
    category = models.CharField(
        max_length = 64,
    )
    author = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
    )
    open = models.BooleanField(
        default = True,
    )

    
class Oferta(models.Model):
    text = models.CharField(
        max_length = 64,
        default="none",
        null=True,
    )
    subasta = models.ForeignKey(
        Subasta,
        on_delete=models.CASCADE,
        null=True,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
    )
    bid = models.IntegerField(
        null=True,
    )


class Comentario(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    text = models.CharField(
        max_length = 64,
    )
    subasta = models.ForeignKey(
        Subasta,
        on_delete=models.CASCADE,
    )