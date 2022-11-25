from rest_framework import serializers
from hospital.models import *
from user_auth.models import *


class AddHospital(serializers.ModelSerializer):
    class Meta:
        model = HospitalData
        fields="__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['created_by'] = {
        'id':instance.created_by.pk,
        'user_name':instance.created_by.first_name
        }
        return response

class AddFloor(serializers.ModelSerializer):
    class Meta:
        model = FloorData
        fields="__all__"

    def to_representation(self, instance):
        print(instance)
        response = super().to_representation(instance)
        response['hospital_id'] = {
        'id':instance.hospital_id.pk,
        'name':instance.hospital_id.name
        }
        return response
           
class AddWard(serializers.ModelSerializer):
    class Meta:
        model = WardData
        fields="__all__"

    def to_representation(self, instance):
        print(instance)
        response = super().to_representation(instance)
        response['hospital_id'] = {
        'id':instance.hospital_id.pk,
        'name':instance.hospital_id.name
        }
        return response

class AddBed(serializers.ModelSerializer):
    class Meta:
        model = BedData
        fields="__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['hospital_id'] = {
        'id':instance.hospital_id.pk,
        'name':instance.hospital_id.name
        }
        return response

class NotificationHistory(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields="__all__"

    
# class AddNotifications(serializers.ModelSerializer):
#     class Meta:
#         model = Notification
#         fields="__all__"

class HospitalDetails(serializers.ModelSerializer):
    class Meta:
        model = HospitalData
        fields="__all__"

    def to_representation(self, instance):
        print(instance)
        response = super().to_representation(instance)
        response['created_by'] = {
        'id':instance.created_by.pk,
        'user_name':instance.created_by.first_name
        }
        if FloorData.objects.filter(hospital_id = int(instance.id)).exists():
            floor_obj = FloorData.objects.filter(hospital_id = int(instance.id))
            floors = []
            for i in floor_obj:
                floors.append(
                {
                    "total_floors" : i.total_floors
               })
            response['floor_details'] = {
                'total_floors' : floors
            }
        if WardData.objects.filter(hospital_id = int(instance.id)).exists():
            ward_obj = WardData.objects.filter(hospital_id = int(instance.id))
            ward_details = []
            for i in ward_obj:
                ward_details.append(
                    {
                        "floor" : i.floor,
                        "ward_name" : i.ward_name,
                        "ward_desc" : i.ward_desc,
                        "led" : i.led
                    }
                )
            response['ward_details'] = {
                'ward_details' : ward_details
            }
        if BedData.objects.filter(hospital_id = int(instance.id)).exists():
            bed_obj =  BedData.objects.filter(hospital_id = int(instance.id))
            bed_details = []
            for i in bed_obj:
                bed_details.append(
                    {
                        "floor" : i.floor,
                        "bed_no" : i.bed_no,
                        "bed_desc" : i.bed_desc,
                        "remote" : i.remote
                    }
                )
                response['bed_details'] = {
                    'bed_details' : bed_details
                }
        
        return response



    