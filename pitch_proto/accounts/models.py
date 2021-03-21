from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    friends = models.ManyToManyField("User", blank=True)
    image = models.ImageField(upload_to='profile_images')
    def __str__(self):
        return self.username

# Create your models here.
class Friend_Request(models.Model):
    from_user = models.ForeignKey(
        User, related_name='from_user', on_delete=models.CASCADE
    )
    to_user = models.ForeignKey(
        User, related_name='to_user', on_delete=models.CASCADE
    )

