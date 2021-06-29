from django.contrib.auth.models import User
from django.db import models

# Create your models here.

AUTH_PROVIDERS = {'facebook': 'facebook', 'google': 'google',
                  'twitter': 'twitter', 'kakao': 'kakao', 'email': 'email'}

class Provider(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    provider_name = models.CharField(max_length=25, blank=False,
                                     null=False, default=AUTH_PROVIDERS.get('email'))
