from django.utils.functional import empty
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from authentication.forms import CustomPasswordResetForm
from enum import unique
from django.conf import settings
from django.db import transaction
from django.db import models
from django.db.models import fields
from rest_framework import serializers, validators
from dj_rest_auth.registration.serializers import RegisterSerializer
from .models import GENDER_SELECTION, Profile
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from dj_rest_auth.serializers import PasswordResetSerializer, PasswordResetConfirmSerializer
from allauth.account.forms import ResetPasswordForm
from django.contrib.auth.forms import PasswordResetForm
from django.utils.translation import gettext as _
# from rest_framework_simplejwt.settings import api_settings
User = get_user_model()

class UserRegistrationSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)
    email = serializers.EmailField(validators=[validators.UniqueValidator(queryset=User.objects.all(), 
                                            message="Email has already been taken")])
    # email = serializers.EmailField()
    username = serializers.CharField(max_length=50, validators=[validators.UniqueValidator(queryset=User.objects.all(), 
                                            message="Username has been taken")])
    gender = serializers.ChoiceField(GENDER_SELECTION, required=False)
    phone = serializers.CharField(max_length=11, required=False)
    address = serializers.CharField(max_length=300, required=False)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
     # The client should not be able to send a token along with a registration
    # request. Making `token` read-only handles that for us.
    # token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        fields = ('first_name', 'last_name', 'username', 'email', 'password', )

    
    # def validate_email(self, value):
    #     user = User.objects.filter(email__iexact=value)
    #     if user.exists():
    #         raise serializers.ValidationError({"email": "Email has already been taken"})
    #     return value
    


    # Override the validate method to check if passowrds match 
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs
    
    def validate_username(self, value):
        if not value.isalnum():
            raise serializers.ValidationError(_('The username should only contain alphanumeric characters'))

    # Define transaction.atomic to rollback the save operation in case of error
    @transaction.atomic
    def create(self, validated_data):
        user = User(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            username=validated_data['username']
            
        )
        # set password
        user.set_password(validated_data['password'])
        user.save()

        # create a user profile
        profile = Profile.objects.create(
            user = user,
            phone = validated_data['phone'],
            address = validated_data['address'],
            gender=validated_data['gender'],

        )

        return user, profile

class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer to enable a user to update their passwords
    """
    # model = User

    old_password = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    password2 = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields do not match"})
        
        return attrs

    # def validate_old_password(self, value):
    
    #     if value == None:
    #         raise serializers.ValidationError({"old_password": "Please enter your current password"})

class CustomPasswordResetSerializer(PasswordResetSerializer):
    """
    Serializer to send a reset link to a user
    """
    password_reset_form_class = CustomPasswordResetForm

    def validate_email(self, value):
        self.reset_form = self.password_reset_form_class(data=self.initial_data)
        if not self.reset_form.is_valid():
            raise serializers.ValidationError(_('Invalid email'))
        # check if user emmail exists in DB
        user = User.objects.filter(email=value)
        if not user.exists():
            raise serializers.ValidationError(_("Email does not exist"))
        return value

    def get_email_options(self):
        request = self.context.get('request')

        return {
            'from_email': getattr(settings, 'MAIL_FROM_ADDRESS'),
            'html_email_template_name': 'authentication/email/password_reset_form.html',
            'request': request,
        }

# class CustomPasswordResetConfirm(PasswordResetConfirmSerializer):


    
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=True)

    def validate(self, attrs):
            if not attrs['refresh']:
                raise serializers.ValidationError(_('Refresh token not found'))
            self.token = attrs['refresh']

            return attrs
       

    def save(self, **kwargs):
        try:
            token = self.token
            return RefreshToken(token).blacklist()

        except TokenError:
            raise serializers.ValidationError({"message" :"Invalid token sent"})




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email',)

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('gender', 'address',)