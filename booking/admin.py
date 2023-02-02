from django.contrib import admin
from .models import Booking_Confirmation,TimeSlot,TurfDetails
# Register your models here.
admin.site.register(Booking_Confirmation)
admin.site.register(TimeSlot)
admin.site.register(TurfDetails)