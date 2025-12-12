import requests
from django.conf import settings
from accounts.models import CustomUser
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken


class GoogleAuthService:
    
    @staticmethod
    def generate_google_auth_url():
        url = f'https://accounts.google.com/o/oauth2/v2/auth?'\
                f'client_id={settings.GOOGLE_CLIENT_ID}&'\
                f'redirect_uri={settings.GOOGLE_REDIRECT_URL}&'\
                'scope=email profile&'\
                'response_type=code'
        return url
    
    @staticmethod
    def get_access_token(code: str):
        data = {
            'client_id': settings.GOOGLE_CLIENT_ID,
            'client_secret': settings.GOOGLE_SECRET,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': settings.GOOGLE_REDIRECT_URL,
        }
        response = requests.post(settings.GOOGLE_TOKEN_URL, data=data)

        if response.status_code != 200:
            return False
        
        access_token = response.json()['access_token']
        return access_token
    
    @staticmethod
    def get_user_info(access_token: str):
        response = requests.get(settings.GOOGLE_USER_INFO_URL, headers={'Authorization': f'Bearer {access_token}'})

        if response.status_code != 200:
            return False

        user = response.json()
        return user

    @staticmethod
    def get_user(user_info):
        user, created = CustomUser.objects.get_or_create(
            username=user_info['email'],
            defaults={
                'email': user_info['email'],
                'first_name': user_info.get('given_name', ''),
                'last_name': user_info.get('family_name', ''),
                'profile_picture': user_info.get('picture', ''),
            }
        )

        return user
    
    @staticmethod
    def get_token(user):
        tokens = {
            'access': str(AccessToken.for_user(user)),
            'refresh': str(RefreshToken.for_user(user))
        }

        return tokens

    @staticmethod
    def login_by_google(code: str):
        access_token = GoogleAuthService.get_access_token(code)
        user_info = GoogleAuthService.get_user_info(access_token)
        user = GoogleAuthService.get_user(user_info)
        tokens = GoogleAuthService.get_token(user)

        return tokens
    