import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from accounts.permissions import IsAdmin, IsManager, IsUser


class UserProfielView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsUser]

    def get(self, request: Request) -> Response:
        return Response({'message': 'hello world'})


class UserProfieUpdatelView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdmin]

    def put(self, request: Request) -> Response:
        # udpate profile
        return Response({'message': 'hello world'})


class GoogleLoginView(APIView):
    
    def post(self, request: Request) -> Response:
        url = f'https://accounts.google.com/o/oauth2/v2/auth?'\
                f'client_id={settings.GOOGLE_CLIENT_ID}&'\
                f'redirect_uri={settings.GOOGLE_REDIRECT_URL}&'\
                'scope=email profile&'\
                'response_type=code'        
        return Response(
            {
                'message': 'google orqali auth qilish uchun link',
                'google_auth_link': url
            }
        )


class GoogleCallbackView(APIView):

    def get(self, request: Request) -> Response:
        code = request.query_params.get('code')
        if code is None:
            return Response({'error': 'code is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        data = {
            'client_id': settings.GOOGLE_CLIENT_ID,
            'client_secret': settings.GOOGLE_SECRET,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': settings.GOOGLE_REDIRECT_URL,
        }
        access_token = requests.post(settings.GOOGLE_TOKEN_URL, data=data).json()['access_token']
        
        return Response({'token': access_token})
