from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication

from accounts.permissions import IsAdmin, IsUser
from .auth_services import GoogleAuthService


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
        url = GoogleAuthService.generate_google_auth_url()
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
        
        tokens = GoogleAuthService.login_by_google(code)
        return Response({'tokens': tokens})
