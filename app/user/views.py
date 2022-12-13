from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.settings import api_settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from user.serializers import (
    UserSerializer,
    AuthTokenSerializer,
    CustomUserSerializer
)


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer


class Login(ObtainAuthToken):
    """Login with token"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    def post(self, request, *args, **kwargs):
        login_serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )
        if login_serializer.is_valid():
            user = login_serializer.validated_data['user']
            if user.is_active:
                token, created = Token.objects.get_or_create(user=user)
                user_serializer = CustomUserSerializer(user)
                if created:
                    return Response({
                        'token': token.key,
                        'user': user_serializer.data,
                        'message': 'Inicio de sesion exitoso!'
                    }, status=status.HTTP_201_CREATED)
                else:
                    token.delete()
                    token = Token.objects.create(user=user)
                    return Response({
                        'token': token.key,
                        'user': user_serializer.data,
                        'message': 'Inicio de sesion exitoso!'
                    }, status=status.HTTP_201_CREATED)
            else:
                return Response(
                    {'error': 'Este usuario no puede iniciar sesion'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        return Response(
            {'error': 'Nombre de usuario o contraseña incorrectos'},
            status=status.HTTP_400_BAD_REQUEST
        )


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user """
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user


class Logout(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            token = request.POST.get('token', '')
            token = Token.objects.filter(key=token).first()
            if token:
                token.delete()
                message = 'Cierre de sesión Exitoso'
                return Response(
                    {'Mensaje': message},
                    status=status.HTTP_200_OK
                )
            return Response(
                {'Error': 'No se encontró usuario con estas credenciales.'},
                status=status.HTTP_409_CONFLICT
            )
        except:
            return Response(
                {'Error': 'No se encontró usuario con estas credenciales.'},
                status=status.HTTP_409_CONFLICT
            )
