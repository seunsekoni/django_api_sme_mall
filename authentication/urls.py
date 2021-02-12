from django.urls import path
# from rest_framework_simplejwt.views import TokenObtainPairView
from .views import MyTokenObtainPairView


app_name='authentication'

urlpatterns= [
    # path('login/', TokenObtainPairView.as_view(), name='login'),
    path('login/', MyTokenObtainPairView.as_view(), name='login'),
]