from django.urls import path
from . import views

app_name = 'client_requests'

urlpatterns = [
    path('fetch-orders/', views.FetchPendingOrdersView.as_view(), name="pending-orders"),
    path('create-order/', views.CreateNewOrderView.as_view(), name="create-order"),
]