from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import UserRegistrationView, UserLoginView, UserDetailView

urlpatterns = [
path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
path('register/', UserRegistrationView.as_view(), name='user_registration'),
path('login/', UserLoginView.as_view(), name='user_login'),
path('user/str:username/', UserDetailView.as_view(), name='user_detail'),
]