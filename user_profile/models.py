from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    bio = models.TextField(blank=True)
    profile_pic = models.ImageField(blank=True, default="images/profile/default_profile_pic.jpg",
                                    upload_to="images/profile/")
    website_url = models.CharField(max_length=200, blank=True, default='')
    facebook_url = models.CharField(max_length=200, blank=True, default='')
    twitter_url = models.CharField(max_length=200, blank=True, default='')

    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        return reverse('index')
