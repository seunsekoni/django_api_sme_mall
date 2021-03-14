from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView
# from dj_rest_auth.registration import views as dj_rest_views


app_name='authentication'

urlpatterns= [
    path('login/', views.MyTokenObtainPairView.as_view(), name='login'),
    path('refresh/token/', TokenRefreshView.as_view(), name='refresh_token'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('change_password/<int:pk>/', views.ChangePasswordView.as_view(), name="change_password"),
    path('password/reset/', views.CustomPasswordResetView.as_view(), name="reset_password"),
    path('confirm/reset/password/', views.CustomPasswordResetConfirmView.as_view(), name="confirm_reset_password")

    # path('dj_rest_auth/', include('dj_rest_auth.urls')),
]