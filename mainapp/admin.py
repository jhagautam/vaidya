from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
# Register your models here.
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(User)
admin.site.register(Appointment)
