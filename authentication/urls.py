from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView
from dj_rest_auth.registration import views as dj_rest_views


app_name='authentication'

urlpatterns= [
    path('login/', views.MyTokenObtainPairView.as_view(), name='login'),
    path('refresh/token/', TokenRefreshView.as_view(), name='refresh_token'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('change_password/<int:pk>/', views.ChangePasswordView.as_view(), name="change_password"),
    path('password/reset/', views.CustomPasswordResetView.as_view(), name="reset_password"),
    path('password/reset/', views.CustomPasswordResetView.as_view(), name="reset_password"),
    path('send/verification-email', views.VerifyEmail.as_view(), name="account_email_verification_sent"),
    path('resend/verification-email/', views.ResendEmailVerificationLink.as_view(), name="resend_verivication_link"),
    # path('dj-rest-auth/account-confirm-email/', VerifyEmailView.as_view(), name='account_email_verification_sent')
    # path('verify-email/', views.VerifyEmail.as_view(), name="verify-the-email"),
    path('confirm/reset/password/', views.CustomPasswordResetConfirmView.as_view(), name="confirm_reset_password")

    # path('dj_rest_auth/', include('dj_rest_auth.urls')),
]