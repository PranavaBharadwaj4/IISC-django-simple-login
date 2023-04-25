from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from .models import User, UserManager
from .serializers import UserSerializer
from django.contrib.auth.hashers import check_password

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(username=user_data['username'])
        # print("hi")
        # print(user_data['password'])
        # # user = User.objects.get(username=user_data['username'])
        # user = User.objects.create_user(self, username=user_data['username'],  email=user_data['email'], password=user_data['password'])
        token = Token.objects.create(user=user)
        response_data = {
        'token': token.key, 
        'user': user_data
        }
        return Response(response_data)

class UserLoginView(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)
    def post(self, request):

        username = request.data.get('username')
        print(username)
        password = request.data.get('password')
        print(password)

        # user = authenticate(username=username, password=password)
        user = User.objects.get(username=username)
        print(user.password)
        # user = authenticate(request,username=username, password=password)
        
        # print(user)

        if password== user.password:
            update_last_login(None, user)
            token, created = Token.objects.get_or_create(user=user)
            serializer = UserSerializer(user)
            return Response({
                'token': token.key,
                'user': serializer.data
            })
        else:
            return Response({'error': 'Invalid Credentials'})

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'username'
    

