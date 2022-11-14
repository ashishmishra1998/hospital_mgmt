from django.contrib import admin
from django.urls import path, include
from hospital.views import *
urlpatterns = [
    path('mapdetails/', MapDetails.as_view(), name='mapdetails'),
    path('addMap/', addMap.as_view(), name='addMap'),
    path('notification/', Notification.as_view(), name='notification'),
    path('testSocket/', TestSocket.as_view(), name='testSocket'),
    
]
    
