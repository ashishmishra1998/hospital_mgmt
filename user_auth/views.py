# import email
# import imp
# from logging import exception
# from multiprocessing import context
from urllib import response
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from user_auth.serializers import *
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from user_auth.renderers import UserRenderer

# Generate Token
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# Create your views here.

class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception = True ):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response ({'token': token , 'msg': 'Registration Successfull'}, status=status.HTTP_201_CREATED)
        return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    def post(self, request, format = None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password =serializer.data.get('password')
            user = authenticate(email=email, password=password)
            role = user.role
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token': token , 'msg' : 'Login Successfull','role':role}, status=status.HTTP_200_OK)
            else:
                return Response ({'errors': {'non_field_errors':['Email or password is not valid']}},
                status=status.HTTP_404_NOT_FOUND)
        return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format = None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class MapDetails(APIView):
    def get(self, request, format = None):

        map = {"map":    {
    "gateway":{"serial":"GATE001"},
    "total_floors":2,
    "floors":[    {"name":"ground","total_rooms":2,
        "rooms":[    {"name":"room1","total_beds":2,"leds":{"serial":"LED001"},
            "beds":[    {"name":"bed1","remote":{"serial":"RMT001"}},
                {"name":"bed2","remote":{"serial":"RMT002"}}]},
            {"name":"room2","total_beds":2,"leds":{"serial":"LED002"},
            "beds":[    {"name":"bed1","remote":{"serial":"RMT003"}},
                {"name":"bed2","remote":{"serial":"RMT004"}},
                {"name":"bed3","remote":{"serial":"RMT009"}}]
            }]},
        {"name":"1st","total_rooms":2,
        "rooms":[{"name":"room1","total_beds":2,"leds":{"serial":"LED003"},
            "beds":[    {"name":"bed1","remote":{"serial":"RMT005"}},
                {"name":"bed2","remote":{"serial":"RMT006"}}]},
            {"name":"room2","total_beds":2,"leds":{"serial":"LED004"},
            "beds":[    {"name":"bed1","remote":{"serial":"RMT007"}},
                {"name":"bed2","remote":{"serial":"RMT008"}}]
            }]
        }]
    }
        }
        return Response({'name':'Nurster','address':'Ahmedabad','contact':'1234512345','map':map})