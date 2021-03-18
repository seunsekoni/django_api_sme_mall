from enum import unique
import random
from re import T
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.

class Category(models.Model):
    """ Model to create the category table """
    title = models.CharField(null=False, max_length=200)
    description = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self) -> str:
        return self.title


class Service(models.Model):
    """ Model to create the service table """
    title = models.CharField(null=False, max_length=200)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, related_name="service_category")
    description = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self) -> str:
        return self.title

class Scope(models.Model):
    name = models.CharField(null=False, max_length=250)
    description = models.TextField(null=True)

    def __str__(self) -> str:
        return self.name

class SubService(models.Model):
    """ Model to create the subservice table """
    title = models.CharField(null=False, max_length=200)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, related_name="subservice_category")
    service = models.ForeignKey(Service, on_delete=models.DO_NOTHING, related_name="subservice_service")
    scope = models.ForeignKey(Scope, related_name="scope", on_delete=models.CASCADE)
    price = models.FloatField(null=True)
    highest_price = models.FloatField(null=True)
    lowest_price = models.FloatField(null=True)
    deliverable = models.TextField(null=True)
    requirements = models.TextField(null=True)
    description = models.TextField(null=True)
    shortest_time = models.IntegerField(null=True)
    average_time = models.IntegerField(null=True)
    longest_time = models.IntegerField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self) -> str:
        return self.title

class Order(models.Model):
    """ Model to create orders """
    unique_reference = models.TextField(max_length=200)
    status = models.TextField(default='pending')
    total_amount = models.FloatField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_order")
    description = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self) -> str:
        return self.unique_reference

    def generate_unique_reference(self):
        """ Generate random numbers to get a unique sme reference number """
        ref_num =  str(random.randint(1000000000, 9999999999))
        if Order.objects.filter(unique_reference=ref_num).exists():
            ref_num = str(random.randint(10000000000, 99999999999))
        return ref_num

    def save(self, *args, **kwargs):
        if self.unique_reference is None:
            self.unique_reference = self.generate_unique_reference
        super(Order, self).save(*args, **kwargs)

class InformationComplaint(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True)

    def __str__(self) -> str:
        return self.name

class Commission(models.Model):
    name = models.CharField(max_length=200)
    sp_percentage = models.FloatField()
    sme_percentage = models.FloatField()
    description = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self) -> str:
        return self.name

class TransactionType(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True)

    def __str__(self) -> str:
        return self.name

CLIENT_STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('open', 'Open'),
    ('accepted', 'Accepted'),
    ('assigned', 'Assigned'),
    ('pending_completion_approval', 'Pending Completion Approval'),
    ('completed', 'completed'),

]

class ClientRequest(models.Model):
    user = models.ForeignKey(User, related_name='user_request', on_delete=models.CASCADE)
    amount = models.FloatField(null=True)
    service = models.ForeignKey(Service, related_name="service_request", on_delete=models.CASCADE)
    sub_service = models.ForeignKey(SubService, related_name="sub_service_request", on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name="category_request", on_delete=models.CASCADE)
    order_reference = models.TextField(max_length=200)
    description = models.TextField(null=True)
    status = models.CharField(choices=CLIENT_STATUS_CHOICES, default='pending', max_length=50)
    assigned_user = models.ForeignKey(User, related_name='service_provider_request', on_delete=models.CASCADE, null=True)
    scope = models.ForeignKey(Scope, on_delete=models.CASCADE, null=True, related_name="scope_request")
    project_duration = models.IntegerField(null=True)
    payment_status = models.BooleanField(default=0)
    sme_reference_num = models.CharField(max_length=20)
    admin_confirm_completion = models.BooleanField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.sme_reference_num

    def generate_sme_reference(self):
        """ Generate random numbers to get a unique sme reference number """
        ref_num =  'sme'+str(random.randint(1000000000, 9999999999))
        if ClientRequest.objects.filter(sme_reference_num=ref_num).exists():
            ref_num = 'sme'+str(random.randint(10000000000, 99999999999))
        return ref_num

    def save(self, *args, **kwargs):
        if self.sme_reference_num is None:
            self.sme_reference_num = self.generate_sme_reference()
        super(ClientRequest, self).save(*args, **kwargs) 

    
