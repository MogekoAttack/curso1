from django.db import models
from django.contrib.auth.models import User as DjangoUser

# Create your models here.

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
