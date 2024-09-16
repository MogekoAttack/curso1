from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.contrib.auth.models import User as DjangoUser

# Create your models here.

class User(AbstractUser):
    groups = models.ManyToManyField(
        Group,
        related_name='grupo_personalizado',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_query_name='user_groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='permisos_personalizados',
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='user_permissions',
    )

class Veterinian(models.Model):
    user = models.ForeignKey(
        DjangoUser,
        blank=False,
        null=False,
        default=0,
        on_delete=models.CASCADE,
    )

    profesional_id = models.CharField(
        max_length=32,
        blank=False,
        null=False,
        default="0",
    )
