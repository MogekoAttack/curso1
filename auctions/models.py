from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Subasta(models.Model):
    text = models.CharField(
        max_length = 64,
    )
    
class Oferta(models.Model):
    text = models.CharField(
        max_length = 64,
    )

class Comentario(models.Model):
    text = models.CharField(
        max_length = 64,
    )