from django.db import models
from django.contrib.auth.models import User

def user_directory_path(instance, filename): 
    return 'user_{0}/{1}'.format(instance.user.id, filename) 

# Create your models here.

class Pet(models.Model):
    name = models.CharField(
        max_length=32,
        verbose_name='Pet name:',
    )

    photo = models.ImageField(
        upload_to=user_directory_path,
        verbose_name='Ingrese la foto de su mascota',
        blank=True,
        null=True,
    )

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='owner',
    )

class Milestone(models.Model):
    name = models.CharField(
        max_length=32,
        verbose_name='Nombre del evento',
    )

    description = models.TextField(
        max_length=2048,
        verbose_name='Ingrese con detalle la descripccion del evento',
    )

    date = models.DateField(
        blank=True,
    )

    pet = models.ForeignKey(
        Pet,
        on_delete=models.CASCADE,
        related_name='milestones'
    )