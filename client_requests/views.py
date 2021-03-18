from client_requests.models import ClientRequest, Order, SubService
from rest_framework.response import Response
from client_requests.serializers import CreateNewOrderSerializer, FetchPendingOrdersSerializer
from django.shortcuts import render
from rest_framework import generics, permissions, serializers, status
from .permissions import isAuthenticatedAndEmailVerified

# Create your views here.
class FetchPendingOrdersView(generics.ListAPIView):
    permission_classes = (isAuthenticatedAndEmailVerified,)
    serializer_class = FetchPendingOrdersSerializer

    def get(self, request):
        data = Order.objects.filter(user=self.request.user)
        response = {
            'success': True,
            "data": FetchPendingOrdersSerializer(data, many=True).data,
            'message':"Successfully retrieved"
        }
        return Response(response, status=status.HTTP_200_OK)

class CreateNewOrderView(generics.ListCreateAPIView):
    serializer_class = CreateNewOrderSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

        

        # get the id of the 
        # print(serializer.data['description'])
        # print(request.data)
            
        # order = Order.objects.create(
        #     user = request.user,
        #     description=serializer.data['description'],
        #     total_amount=40000
        # )
        # order.unique_reference = order.generate_unique_reference()
        # order.save()

        return Response({'message': "Order created"})

