from django.db import models
from user_auth.models import *

class HospitalData(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    contact = models.CharField(max_length=12)
    email = models.EmailField(max_length=100)
    created_by = models.ForeignKey(User_data, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class FloorData(models.Model):
    total_floors = models.CharField(max_length=100)
    hospital_id = models.ForeignKey(HospitalData, on_delete=models.CASCADE)

class WardData(models.Model):
    floor = models.CharField(max_length=100)
    ward_name = models.CharField(max_length=100)
    ward_desc = models.CharField(max_length=100)
    led = models.CharField(max_length=150)
    hospital_id = models.ForeignKey(HospitalData, on_delete=models.CASCADE)

class BedData(models.Model):
    floor = models.CharField(max_length=100)
    bed_no = models.CharField(max_length=100)
    bed_desc = models.CharField(max_length=200)
    remote = models.CharField(max_length=150)
    ward_id =  models.ForeignKey(WardData, on_delete=models.SET_NULL, null=True)
    hospital_id = models.ForeignKey(HospitalData, on_delete=models.CASCADE)

class Notification(models.Model):
    event = models.CharField(max_length=25)
    type = models.CharField(max_length=30)
    serial = models.CharField(max_length=40)
    time = models.DateTimeField(null=True, blank=True)
    card_serial = models.CharField(max_length=20) 


    

