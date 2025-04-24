from rest_framework import serializers
from django.contrib.auth import get_user_model
from .validators import validate_age
from rest_framework_simplejwt.tokens import RefreshToken
from  django.core.mail import send_mail
from decouple import config

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    birth_date = serializers.DateField(validators=[validate_age])

    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','password','birth_date']
        extra_kwargs = {
            "password": {
                "write_only":True
            }
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.is_active=False
        user.save()

        token = RefreshToken.for_user(user).access_token
        verification_link = f"http://localhost:8000/api/accounts/verify-email/?token={str(token)}"

        send_mail(
                "Verify your Email",
                f"Click the link to verify your email: {verification_link}",
                config('EMAIL_HOST_USER'),
                [user.email],
                fail_silently=False
            )
        
        return user
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, data):
        user = User.objects.filter(email=data['email']).first()

        if not user:
            return serializers.ValidationError("user not found")
        if not user.is_active:
            return serializers.ValidationError("email not verified")
        if not user.check_password(data['password']):
            return serializers.ValidationError('incorrect password')

        return user