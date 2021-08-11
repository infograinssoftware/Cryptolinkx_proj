from django.contrib import admin
from .models import User_OTP, User_qrcode, User_KYC

@admin.register(User_OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ['user', 'email', 'otp']

admin.site.register(User_qrcode)

@admin.register(User_KYC)
class KYCADMIN(admin.ModelAdmin):
    list_display = ['user','document_type','id_number']