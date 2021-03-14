import re
from dj_rest_auth.serializers import PasswordResetConfirmSerializer
from django.http.response import JsonResponse
from django.shortcuts import render
from rest_framework import generics, serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.state import User
from rest_framework_simplejwt.views import TokenObtainPairView
from .helpers import sendResponse
from .serializers import ChangePasswordSerializer, CustomPasswordResetSerializer, LogoutSerializer, UserRegistrationSerializer, UserSerializer, ProfileSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import permissions
from django.core.mail import send_mail
from django.template.loader import render_to_string
from dj_rest_auth.views import PasswordResetView



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

        # send mail to new user

        msg_html = render_to_string('authentication/email/welcome_mail.html', {'user': user})

        send_mail(
            'Welcome To The SME MALL',
            '',
            'testing@sender',
            [user.email],
            html_message=msg_html,
        )
        
        return Response({
            'user': UserSerializer(user,context=self.get_serializer_context()).data,
            'token': res,
            'profile':ProfileSerializer(profile,context=self.get_serializer_context()).data
        })

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



