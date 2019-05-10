import requests
from uuid import uuid4

from django.contrib.auth import authenticate, login
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from rest_framework import viewsets, status
from rest_framework.decorators import list_route
from rest_framework.response import Response

from apps.users.models import User
from apps.users.serializers import UserSerializer, UserWriteSerializer

from apps.misc.logger import *

logger = logging.getLogger(__name__)
logger.addHandler(handler)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return UserSerializer
        return UserWriteSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(self.request.data.get('password'))
        user.save()

    def perform_update(self, serializer):
        user = serializer.save()
        if 'password' in self.request.data:
            user.set_password(self.request.data.get('password'))
            user.save()

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

    @list_route(methods=['GET'])
    def profile(self, request):
        if request.user.is_authenticated:
            serializer = self.serializer_class(request.user)
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    @list_route(methods=['POST'])
    def register(self, request):
        try:
            last_name = request.data.get('lastName', None)
            first_name = request.data.get('firstName', None)
            email = request.data.get('email', None)
            password = request.data.get('password', '')

            if(password == ''):
                password = User.objects.make_random_password()

            if User.objects.filter(email__iexact=email).exists():
                return Response({'status': 210})

            # user creation
            receivedData = dict()
            receivedData["last_name"] = last_name
            receivedData["first_name"] = first_name
            receivedData["email"] = email
            receivedData["password"] = password

            serializer = self.serializer_class(data=receivedData)
            if(
                serializer.is_valid()
            ):     
                user = serializer.save()
                
                user.set_password(password)
                user.save()

                return Response(
                    UserSerializer(user).data,
                    status=status.HTTP_201_CREATED
                )
            else:
                logger.error("serializer.errors: " + str(serializer.errors))
                return Response(
                    status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as e:
            logger.error('Exception: ' + str(e))
            return Response(
                status=status.HTTP_400_BAD_REQUEST
            )


        

    @list_route(methods=['POST'])
    def password_reset(self, request, format=None):
        if User.objects.filter(email=request.data['email']).exists():
            user = User.objects.get(email=request.data['email'])
            params = {'user': user, 'DOMAIN': settings.DOMAIN}
            send_mail(
                subject='Password reset',
                message=render_to_string('mail/password_reset.txt', params),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[request.data['email']],
            )
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @list_route(methods=['POST'])
    def password_change(self, request, format=None):
        if User.objects.filter(token=request.data['token']).exists():
            user = User.objects.get(token=request.data['token'])
            user.set_password(request.data['password'])
            user.token = uuid4()
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
