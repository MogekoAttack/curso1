from django.db import models

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
    )

    