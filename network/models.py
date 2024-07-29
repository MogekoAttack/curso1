from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name="usuario")
    content = models.TextField(blank=False)
    created = models.DateField(auto_now_add=True, null=True)
    likes = models.IntegerField(default=0,editable=False, null=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    followers = models.ManyToManyField(User, related_name='following', blank=True)

    

User.profile = property(lambda u: Profile.objects.get_or_create(user=u)[0])