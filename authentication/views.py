import re
from allauth.account.models import EmailAddress
from dj_rest_auth.serializers import PasswordResetConfirmSerializer
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.conf import settings
from django.http.response import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse
from rest_framework import generics, serializers, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.state import User
from rest_framework_simplejwt.views import TokenObtainPairView
from .helpers import sendResponse
from .serializers import ChangePasswordSerializer, CustomPasswordResetSerializer, LogoutSerializer, UserRegistrationSerializer, UserSerializer, ProfileSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import Utils
import jwt
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication




# Create your views here.
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['name'] = user.email

        return token

    def validate(self, attrs):
        # The default result (access/refresh tokens)
        data = super(MyTokenObtainPairSerializer, self).validate(attrs)

        # Custom data to be included
        data.update({'user': UserSerializer(self.user).data})
        data.update({'profile': ProfileSerializer(self.user.user_profile).data})


        return data
        
        # return sendResponse(data, 'successfully')

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]


    def post(self,request,*args,**kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        user,profile = serializer.save()
        refresh = RefreshToken.for_user(user)
        res = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

        # send welcome mail to new user
        email_subject = "Welcome to the SME Mall"
        msg_html = render_to_string('authentication/email/welcome_mail.html', {'user': user})

        data = {
            'user_email': user.email,
            'email_subject': email_subject,
            'msg_html': msg_html
        }
        Utils.send_the_email(data)

        # send verification email

        current_site = get_current_site(request).domain
        # get the url 
        relative_link = reverse('authentication:account_email_verification_sent')
        protocol = request.scheme
        
        absolute_url = f"{protocol}://{current_site}{relative_link}?token={res['access']}"
        email_subject = "Verify your Email Address"
        msg_html = render_to_string('authentication/email/verification_sent.html', {
                                                                    'user': user,
                                                                    'link': absolute_url,

                                                                    })

        email_verification_data = {
            'user_email': user.email,
            'email_subject': email_subject,
            'msg_html': msg_html,
        }

        Utils.send_the_email(email_verification_data)

        

        # msg_html = render_to_string('authentication/email/welcome_mail.html', {'user': user})

        # send_mail(
        #     'Welcome To The SME MALL',
        #     '',
        #     'testing@sender',
        #     [user.email],
        #     html_message=msg_html,
        # )
        
        return Response({
            'user': UserSerializer(user,context=self.get_serializer_context()).data,
            'token': res,
            'profile':ProfileSerializer(profile,context=self.get_serializer_context()).data
        }, status=status.HTTP_201_CREATED)

class ResendEmailVerificationLink(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    def post(self, request):
        user = request.user
        # token = JWTTokenUserAuthentication.get_header(self, request)
        # print(token)
        # token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
        # data = {'token': token}

        refresh = RefreshToken.for_user(user)
        # print(refresh.access_token)

        current_site = get_current_site(request).domain

        relative_link = reverse('authentication:account_email_verification_sent')

        protocol = request.scheme
        
        absolute_url = f"{protocol}://{current_site}{relative_link}?token={refresh.access_token}"
        email_subject = "Verify your Email Address"
        msg_html = render_to_string('authentication/email/verification_sent.html', {
                                                                    'user': user,
                                                                    'link': absolute_url,

                                                                    })

        email_verification_data = {
            'user_email': user.email,
            'email_subject': email_subject,
            'msg_html': msg_html,
        }

        Utils.send_the_email(email_verification_data)

        
        return Response({
            'success': True,
            'message': "Verification link has been sent to your email address"
        }, status=status.HTTP_200_OK)




class VerifyEmail(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    def get(self, request):
        try:
            token = request.GET.get('token')
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = User.objects.get(id=payload['user_id'])
            if user.id != payload['user_id']:
                raise InvalidToken('The token is invalid')

            if user.is_verified:
                raise PermissionDenied('Your account has been previously verified')

            if not user.is_verified:
                user.is_verified = True
                user.save()

                
            
            response = {
                'success': True,
                'message': 'Successfully verified user'
            }
            return Response(response, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            response = {
                'success': False,
                'message': 'Token Expired'
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        # if user tampered with the token
        except jwt.DecodeError:
            response = {
                'success': False,
                'message': 'Invalid Token'
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

class ChangePasswordView(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        # print(request.__dict__)
        self.object = self.get_object()
        serialized = self.get_serializer(data=request.data)

        if serialized.is_valid(raise_exception=True):
            # serialized.save()
            # check if old passwords corresponds
            if not self.object.check_password(serialized.data.get('old_password')):
                raise serializers.ValidationError({"old_password": "Wrong Password"})
            self.object.set_password(serialized.data.get('password'))
            self.object.save()
            response = {
                    'status': True,
                    'code': status.HTTP_200_OK,
                    'message': 'Password updated successfully',
                    'data': []
            }
            return Response(response)

class CustomPasswordResetView(generics.CreateAPIView):
    serializer_class = CustomPasswordResetSerializer
    permission_classes = (permissions.AllowAny, )

    def post(self, request, *args, **kwargs):
        serialized = self.get_serializer(data=request.data)
        if serialized.is_valid(raise_exception=True):
            serialized.save()
            response = {
                'status': True,
                'code': status.HTTP_200_OK,
                'message': 'Reset link has been sent to your email',
                'data': []
            }
            return Response(response)

class CustomPasswordResetConfirmView(generics.CreateAPIView):
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = (permissions.AllowAny,)
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            response = {
                'status': True,
                'code': status.HTTP_200_OK,
                'message': 'Password has been successfully reset',
                'data': []
            }
            return Response(response)


# class CustomPasswordResetView(PasswordResetView):
#     serializer_class = CustomPasswordResetSerializer
#     permission_classes = (permissions.AllowAny, )


class LogoutView(generics.DestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = LogoutSerializer
    queryset = User.objects.all()


    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if(serializer.is_valid(raise_exception=True)):
            serializer.save()

            return Response({
                'status':status.HTTP_205_RESET_CONTENT,
                "message" : "Successfully logged out"
            })
        # except Exception as e:
        #     return Response(status=status.HTTP_400_BAD_REQUEST)



