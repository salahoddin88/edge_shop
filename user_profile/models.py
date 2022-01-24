from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="UserProfile")
    address = models.TextField(null=True, blank=True)
    mobile = models.CharField(max_length=10, null=True, blank=True)
    profile_picture = models.ImageField(null=True, blank=True)

    def __str__(self):
        """ Default User model will return User's username """
        return (self.user.first_name)