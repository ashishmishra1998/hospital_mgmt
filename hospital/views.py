from django.shortcuts import render
from urllib import response
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from hospital.serializers import *
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from user_auth.renderers import UserRenderer

# Create your views here.


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

class Notification(APIView):
    def post(self, request, format=None):
        #  serializer = NotificationSerializer(data=request.data)
        data = {"total_events":2,
        "events":[{"event": "NURSE_CALL","type": "remote", "serial": "RMT002", "time": 1000},
        {"event": "DOCTOR_CALL","type": "remote", "serial": "RMT003", "time": 1000}]}

        return Response({"data":data})
