from django.db import transaction
from django.shortcuts import get_object_or_404
from client_requests.models import Category, ClientRequest, Order, Service, SubService
from django.db.models import fields
from rest_framework import serializers

class FetchPendingOrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

    # def create(self, validated_data):

class CreateNewOrderSerializer(serializers.Serializer):
    sub_service_id = serializers.ListField()
    description = serializers.CharField()

    def validate_sub_service_id(self, value):
        if value is None:
            raise serializers.ValidationError(_('subservice is required'))
        return value

    @transaction.atomic
    def create(self, validated_data):
        subservices = validated_data['sub_service_id']
        user = self.context.get('request').user
        # print('stop')

        # create the order

        order = Order.objects.create(
            user = user,
            description=validated_data['description'],
            
        )
        order.unique_reference = order.generate_unique_reference()
        order.save()

        total_amount = 0
        if isinstance(subservices, list):

            for sub in subservices:
                # subservice = SubService.objects.get(id=1)
                product = get_object_or_404(SubService, pk=sub)
                # print(product.category_id)
                client_request = ClientRequest.objects.create(
                    description=validated_data['description'],
                    user=user,
                    # category= get_object_or_404(Category, pk=product.category_id),
                    category= Category.objects.get(pk=product.category_id),
                    service = Service.objects.get(pk=product.service_id),
                    # service=get_object_or_404(Service, pk=product.service_id),
                    sub_service=product,
                    amount=product.price,
                    project_duration=product.average_time,
                    order_reference=order.unique_reference
                )
                # increment total amount so as to save in the orders table
                total_amount += product.price

        return order






        


# class SubServiceSerializer(serializers.ModelSerializer):

