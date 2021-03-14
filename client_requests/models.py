from enum import unique
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    """ Model to create the category table """
    title = models.CharField(null=False, max_length=200)
    description = models.TextField(null=True)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

class Service(models.Model):
    """ Model to create the service table """
    title = models.CharField(null=False, max_length=200)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, related_name="service_category")
    description = models.TextField(null=True)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

class SubService(models.Model):
    """ Model to create the subservice table """
    title = models.CharField(null=False, max_length=200)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, related_name="subservice_category")
    service = models.ForeignKey(Service, on_delete=models.DO_NOTHING, related_name="subservice_service")
    price = models.FloatField(null=True)
    highest_price = models.FloatField(null=True)
    lowest_price = models.FloatField(null=True)
    deliverable = models.TextField()
    requirements = models.TextField()
    description = models.TextField(null=True)
    shortest_time = models.IntegerField(null=True)
    average_time = models.IntegerField(null=True)
    longest_time = models.IntegerField(null=True)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

class Order(models.Model):
    """ Model to create orders """
    unique_reference = models.TextField(max_length=200)
    status = models.TextField(default='pending')
    total_amount = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_order")
    description = models.TextField()
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)


# class ClientRequest(models.Model):
#     user = models.ForeignKey(User, related_name='user_request', on_delete=models.CASCADE)
#     amount = models.FloatField(null=True)
    # service = 

