from django.contrib import admin
from django.urls import path, include
from hospital.views import *
urlpatterns = [
    path('mapdetails/', MapDetails.as_view(), name='mapdetails'),
    path('addMap/', addMap.as_view(), name='addMap'),
    path('notification/', NotificationData.as_view(), name='notification'),
    path('notificationhistory/', NotificationHistory.as_view(), name='notificationhistory'),
    path('testSocket/', TestSocket.as_view(), name='testSocket'),
    path('addHospital/', addHospital.as_view(), name='addHospital'),
    path('allHospital/', allHospital.as_view(), name='allHospital'),
    path('accessSingleHospital/<int:pk>/', accessSingleHospital.as_view(), name='accessSingleHospital'),
    path('addFloor/', addFloor.as_view(), name='addFloor'),
    path('allHospitalFloors/', allHospitalFloors.as_view(), name='allHospitalFloors'),
    path('accessSingleHospitalFloors/<int:pk>/', accessSingleHospitalFloors.as_view(), name='accessSingleHospitalFloors'),
    path('addWard/', addWard.as_view(), name='addWard'),
    path('allHospitalWards/', allHospitalWards.as_view(), name='allHospitalWards'),
    path('accessSingleHospitalWards/<int:pk>/', accessSingleHospitalWards.as_view(), name='accessSingleHospitalWards'),
    
    path('addBed/', addBed.as_view(), name='addBed'),
    path('allHospitalBeds/', allHospitalBeds.as_view(), name='allHospitalBeds'),
    path('accessSingleHospitalBeds/<int:pk>/', accessSingleHospitalBeds.as_view(), name='accessSingleHospitalBeds'),
    
    path('hospitalDetails/<int:pk>/', hospitalDetails.as_view(), name='hospitalDetails'),
]
    
