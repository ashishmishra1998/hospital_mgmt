from django.contrib import admin

from .models import *
admin.site.register(HospitalData)
admin.site.register(FloorData)
admin.site.register(WardData)
admin.site.register(BedData)
admin.site.register(Notification)

# Register your models here.
