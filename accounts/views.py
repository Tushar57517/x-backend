from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import (
    RegisterSerializer
)
from rest_framework_simplejwt.tokens import AccessToken

User = get_user_model()

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data) 
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"verification link sent."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailView(APIView):
    def get(self, request):
        token = request.GET.get('token')

        try:
            access_token = AccessToken(token)

            user = User.objects.get(id=access_token['user_id'])
            user.is_active = True
            user.save()
            return Response({"message":"email verified successfully"}, status=status.HTTP_200_OK)
        
        except Exception:
            return Response({"error":"invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)