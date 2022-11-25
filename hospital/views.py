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
from .models import *
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

class NotificationData(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        channel_layer = get_channel_layer()
        context = request.data
        event_data = context.get('events')
        for i in event_data:
            event = i['event']
            type =  i['type']
            serial = i['serial']
            time =  i['time']
            card_serial = i['card_serial']
            if Notification.objects.filter(serial = serial).exists():
                notificationobj = Notification.objects.filter(serial = serial).last()
                bed_no = BedData.objects.get(remote = serial)
                floor = bed_no.floor
                bed_id = bed_no.id
                bed_desc = bed_no.bed_desc
                ward_data = bed_no.ward_id
                ward_name =  ward_data.ward_name
                ward_desc = ward_data.ward_desc
                ward_id = ward_data.id
                details = {"card_serial":card_serial,"event":event,"serial":serial,"floor":floor,"bed_id":bed_id,"bed_desc":bed_desc,"ward_name":ward_name,"ward_desc":ward_desc,"ward_id":ward_id}
                if notificationobj.card_serial == "": 
                    notificationobj.card_serial = card_serial
                    notificationobj.save()
                    async_to_sync(channel_layer.group_send)('notification', {
                    'type': 'chat_message',
                    'message':details
                    })
                else:
                    data = Notification.objects.create(event = event, type = type, serial = serial, time = time, card_serial = card_serial)
                    data.save()
                    async_to_sync(channel_layer.group_send)('notification', {
                    'type': 'chat_message',
                    'message':details
                    })
            else:
                data = Notification.objects.create(event = event, type = type, serial = serial, time = time, card_serial = card_serial)
                data.save()   
                async_to_sync(channel_layer.group_send)('notification', {
                    'type': 'chat_message',
                    'message':details
                    })
            return Response({"Message":"Notification Sent!", "data" : request.data})
        return Response({"Message":"Notification Not Sent!"})

class NotificationHistory(ListAPIView):
    serializer_class = NotificationHistory
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Notification.objects.all().order_by('-id')[:10]


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

# def send(data):
#     channel_layer = get_channel_layer()
#     async_to_sync(channel_layer.group_send)('test', {
#             'type': 'chat_message',
#             'message':data
#         })
#     return HttpResponse("sent")

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

# class Notification(CreateAPIView):
#     # serializer_class = AddNotifications
#     permission_classes = [IsAuthenticated]
#     def perform_create(self, serializer):
#         obj = serializer.save()
#         obj.created_by = self.request.user
#         obj.save()


class hospitalDetails(RetrieveAPIView):
    serializer_class = HospitalDetails
    permission_classes = [IsAuthenticated]

    lookup_field ='pk'
    def get_queryset(self):
        return HospitalData.objects.filter(id =  int(self.kwargs['pk']))



    




