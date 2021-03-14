from django.db import models
from django.contrib.auth.models import User


GENDER_SELECTION = [
    ('M', 'Male'),
    ('F', 'Female'),
    ('NS', 'Not Specified'),
]


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, related_name='user_profile', on_delete=models.CASCADE)
    phone = models.CharField(blank=True, null=True, max_length=200)
    address = models.CharField(blank=True, null=True, max_length=250)
    active_service_provider = models.BooleanField(default=False)
    gender = models.CharField(max_length=20, choices=GENDER_SELECTION)

    def __str__(self) -> str:
        return self.user.first_name
    
