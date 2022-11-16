from django.shortcuts import render
from urllib import response
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView,UpdateAPIView,ListAPIView,RetrieveUpdateDestroyAPIView,RetrieveAPIView
from hospital.serializers import *
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from user_auth.renderers import UserRenderer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
from django.http import HttpResponse
from .consumers import NotificationConsumer

# Create your views here.




class MapDetails(APIView):
    permission_classes = [IsAuthenticated]
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
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        #  serializer = NotificationSerializer(data=request.data)
        if request.data:
            return Response({"Message":"Notification Sent!", "data" : request.data})
        return Response({"Message":"Notification Not Sent!"})



class TestSocket(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        #  serializer = NotificationSerializer(data=request.data)
        channel_layer = get_channel_layer()
        
        context = {"name" :  request.data['name'], "mobile_no" :request.data['mobile_no']}
        if request.data:
            
            async_to_sync(channel_layer.group_send)('test', {
            'type': 'chat_message',
            'message':context
        })
            return Response({"Message":"Socket Connected and data sent!", "context" : context })
        return Response({"Message":"Socket Not Connected!"})

# Method and socket

def send(data):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)('test', {
            'type': 'chat_message',
            'message':data
        })
    return HttpResponse("sent")

class addMap(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request, format = None):
        global mapdata
        mapdata = request.data
        if request.data:
            return Response({"Message":"Map Details Saved!"})
        return Response({"Message":"Maps detials not saved"})
    
    def get(self, request, format = None):
        return Response({'map':mapdata})


class addHospital(CreateAPIView):
    serializer_class = AddHospital
    permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        obj = serializer.save()
        obj.created_by = self.request.user
        obj.save()
    
class allHospital(ListAPIView):
    serializer_class = AddHospital
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return HospitalData.objects.all()
    
class accessSingleHospital(RetrieveUpdateDestroyAPIView):
    serializer_class = AddHospital
    permission_classes = [IsAuthenticated]

    lookup_field ='pk'
    def get_queryset(self):
        return HospitalData.objects.filter(id =  int(self.kwargs['pk']))

class addFloor(CreateAPIView):
    serializer_class = AddFloor
    permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        obj = serializer.save()
        obj.created_by = self.request.user
        obj.save()
    
class allHospitalFloors(ListAPIView):
    serializer_class = AddFloor
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FloorData.objects.all()

class accessSingleHospitalFloors(RetrieveUpdateDestroyAPIView):
    serializer_class = AddFloor
    permission_classes = [IsAuthenticated]

    lookup_field ='pk'
    def get_queryset(self):
        return FloorData.objects.filter(id =  int(self.kwargs['pk']))

class addWard(CreateAPIView):
    serializer_class = AddWard
    permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        obj = serializer.save()
        obj.created_by = self.request.user
        obj.save()

class allHospitalWards(ListAPIView):
    serializer_class = AddWard
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return WardData.objects.all()

class accessSingleHospitalWards(RetrieveUpdateDestroyAPIView):
    serializer_class = AddWard
    permission_classes = [IsAuthenticated]

    lookup_field ='pk'
    def get_queryset(self):
        return WardData.objects.filter(id =  int(self.kwargs['pk']))


class addBed(CreateAPIView):
    serializer_class = AddBed
    permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        obj = serializer.save()
        obj.created_by = self.request.user
        obj.save()

class allHospitalBeds(ListAPIView):
    serializer_class = AddBed
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return BedData.objects.all()

class accessSingleHospitalBeds(RetrieveUpdateDestroyAPIView):
    serializer_class = AddBed
    permission_classes = [IsAuthenticated]

    lookup_field ='pk'
    def get_queryset(self):
        return BedData.objects.filter(id =  int(self.kwargs['pk']))



class hospitalDetails(RetrieveAPIView):
    serializer_class = HospitalDetails
    permission_classes = [IsAuthenticated]

    lookup_field ='pk'
    def get_queryset(self):
        return HospitalData.objects.filter(id =  int(self.kwargs['pk']))



    




