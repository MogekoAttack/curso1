from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name="usuario")
    content = models.TextField(blank=False)
    created = models.DateField(auto_now_add=True, null=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    followers = models.ManyToManyField(User, related_name='following', blank=True)

# class Like(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     post_likes = models.ManyToManyField(Post, related_name="post_likes", blank=True)

User.profile = property(lambda u: Profile.objects.get_or_create(user=u)[0])