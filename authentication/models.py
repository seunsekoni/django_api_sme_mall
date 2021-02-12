from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(related_name='user_profile', )
    phone = models.CharField(blank=True, null=True)
    address = models.CharField(blank=True, null=True)
    active_service_provider = models.BooleanField(default=False)
    
