from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    This model is used to represent client users.
    """
    friends = models.ManyToManyField("User", blank=True)
    image = models.ImageField(upload_to='profile_images', default='media/default.jpg')
    dark_mode = models.BooleanField(default=True)
    explicit = models.BooleanField(default=True)
    bio = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.username

# Create your models here.
class Friend_Request(models.Model):
    """
    This model is used for holding open friend requests.
    """
    from_user = models.ForeignKey(
        User, related_name='from_user', on_delete=models.CASCADE
    )
    to_user = models.ForeignKey(
        User, related_name='to_user', on_delete=models.CASCADE
    )

class Follows(models.Model):
    """
    This model is used to implement a follower system.
    """
    follower = models.ForeignKey(
        User, related_name='follower', on_delete=models.CASCADE
    )
    following = models.ForeignKey(
        User, related_name='following', on_delete=models.CASCADE
    )
