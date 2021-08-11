from django.urls import path
from .views import (

 User_Register, 
 User_Login, 
 User_Logout,
 Verify_Otp,
 Resend_Otp,
 Verification,
 Resend_Email,
 email_verified,
 Mobile_Verfication,
 Verify_Mobile_OTP,
 User_KYC_View
 )
 
from django.contrib.auth import views as auth_views

urlpatterns = [
    
    path('register/', User_Register.as_view(), name = 'register'),
    path('login/', User_Login.as_view(), name = 'login'),
    path('logout/', User_Logout.as_view(), name = 'logout'),
    path('verifyotp/', Verify_Otp.as_view(), name = 'verifyotp'),
    path('resend_otp/', Resend_Otp.as_view(), name = 'resend_otp'),
    path('verify/', Verification.as_view(), name = 'verify'),
    path('resend_mail', Resend_Email.as_view(), name = 'resend_mail'),
    path('cryptolinkx/',email_verified, name = 'cryptolinkx'),
    path('mobile_verify/',Mobile_Verfication.as_view(), name = 'mobile_verify'),
    path('mobile_verify_otp/',Verify_Mobile_OTP.as_view(), name = 'mobile_verify_otp'),
    path('user_kyc/', User_KYC_View.as_view(), name = 'user_kyc'),


    #forgot password

     path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='authentication/password_reset.html',
             subject_template_name='authentication/password_reset_subject.txt',
             email_template_name='authentication/password_reset_email.html',
             # success_url='/login/'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='authentication/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='authentication/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='authentication/password_reset_complete.html'
         ),
         name='password_reset_complete'),
]

