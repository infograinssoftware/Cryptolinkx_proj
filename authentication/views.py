from django.shortcuts import render, redirect
from django.views.generic import View
from users.models import Custom_User
from authentication.models import User_OTP, User_qrcode, User_KYC
from django.core.mail import send_mail
from django.conf import settings
import random
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.http import JsonResponse
from django_email_verification import send_email
from django.core.mail import EmailMultiAlternatives
from bitcoin import *
from core.models import Currency_Wallet, CoinPair
import qrcode
import http.client

from bitmerchant.wallet import Wallet
from Cryptolinkx_proj.settings import WALLET_PUBKEY  # Created above

def send_html_email(email, otp):
    print('inside html mail')
    subject, from_email, to = 'Verify OTP To Login CryptolinkX', f'{settings.DEFAULT_FROM_EMAIL}', f'{email}'
    text_content = 'This is an important message.'
    html_content = f'<div style="height:200px; width:100%; font-size:20px; color: white; background-color: black; text-align: center; align-content: center; padding-top:15%;">Your Cryptolinkx OTP Is <strong style="color: white; background-color: black;">{otp}</strong></div>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def send_otp(mobile, otp):

    conn = http.client.HTTPSConnection("api.msg91.com")
    authkey = settings.AUTH_KEY 
    headers = { 'content-type': "application/json" }
    space=" "
    url = f'http://control.msg91.com/api/sendotp.php?otp={otp}&message=Please_verify_your_otp_{otp}&mobile={mobile}&authkey={authkey}&country=91'
    conn.request("GET", url , headers=headers)
    res = conn.getresponse()
    data = res.read()
    print(data)

    return None
# def send_mail_otp(email, otp):

#     send_mail(

#         'Please verify flowcal account',
#         f'Your Flowcal OTP is {otp}',
#         f'{settings.DEFAULT_FROM_EMAIL}',
#         [f'{email}'],
#         fail_silently=False,

#     )
                                  
class User_Register(View):
    template_name = 'authentication/signup.html'

    def get(self, request, *args, **kwargs):

        return render(request, template_name = self.template_name)

    def post(self, request, *args, **kwargs):
        print('ggghhjhkj')
        full_name = request.POST.get('full_name', None).strip()
        email = request.POST.get('email',None).strip()
        password = request.POST.get('password',None).strip()
        cfm_password = request.POST.get('cfm_password',None).strip()
        if (full_name== '' or full_name == None)  or (email== '' or email == None) or (password== '' or password == None) or (cfm_password== '' or cfm_password == None): 
            messages.warning(request, f'{full_name} Please enter full detail', 'warning')
            return redirect('/auth/register', {'full_name': full_name, 'email': email, 'password': password, 'cfm_password' : cfm_password})
        if password == cfm_password:

            if not Custom_User.objects.filter(email = email, is_active = True).exists():

                try:

                    user_obj = Custom_User.objects.create_user(username = full_name, email = email, password = password, is_active = False)
                    
                    # send_html_email(email, otp_gen)
                    send_email(user_obj)

                    otp = random.randint(000000,999999)
                    user_qrcode = User_qrcode.objects.create(user = user_obj, otp = otp)
                    user_qrcode.save()

                    request.session['email'] = email
                    request.session['pass'] = password
                    request.session['active'] = "False"
                    messages.warning(request, 'Verify your mail and Login', 'success')
                    return redirect('/auth/verify/')

                except Exception as e:
                    print(e)
                    user_obj = Custom_User.objects.get(email = email, is_active = False)
                    user_obj.delete()
                    user_obj = Custom_User.objects.create_user(username = full_name, email = email, password = password, is_active = False)

                    # send_html_email(email, otp_gen)
                    send_email(user_obj)
 
                    otp = random.randint(000000,999999)
                    user_qrcode = User_qrcode.objects.create(user = user_obj, otp = otp)
                    user_qrcode.save()

                    request.session['email'] = email
                    request.session['pass'] = password
                    request.session['active'] = "False"
                    messages.warning(request, 'Verify your mail and Login', 'success')
                    return redirect('/auth/verify/')

            else:

                messages.warning(request, 'Email already taken', 'danger')

                return redirect('/auth/register')
        else:
                                                 
            messages.warning(request, 'Unmatched password !', 'danger')

            return render(request, template_name = self.template_name, context = {'full_name': full_name, 'email': email, 'password': password, 'cfm_password' : cfm_password})

        return redirect('/auth/register/')
                                                                                                                        

class Verification(View):
    template_name = 'authentication/verification.html'
    def get(self, request, *args, **kwargs):
        user_qrcode_obj = User_qrcode.objects.filter(user__email = request.user).last()
        if user_qrcode_obj:
            qr_verified = user_qrcode_obj.user.is_qrcode_verified
            otp_verified = user_qrcode_obj.user.is_otp_verified
            return render(request, template_name = self.template_name, context  = {'user_qrcode_obj': user_qrcode_obj, 'qr_verified' : qr_verified, 'otp_verified': otp_verified})

        # user_qrcode_obj = User_qrcode.objects.filter(user__email = request.session.get('email')).last()
        # qr_verified = user_qrcode_obj.user.is_qrcode_verified
        # return render(request, template_name = self.template_name, context  = {'user_qrcode_obj': user_qrcode_obj, 'qr_verified' : qr_verified})

        return render(request, template_name = self.template_name)

def email_verified(request):
        
    if request.method == 'POST':
        qr_otp = request.POST.get('qr_otp')
        user_qrcode_obj = User_qrcode.objects.filter(user__email = request.session.get('email')).last()
        if user_qrcode_obj.otp == int(qr_otp):
            user_qrcode_obj.user.is_qrcode_verified = True
            user_qrcode_obj.user.save()
            return redirect('/auth/verify/')
        else:
            return JsonResponse({'msg' : 'Wrong OTP'})

    else:
        request.session['active'] = "True"
        user = authenticate(email = request.session['email'], password = request.session.get('pass'))
        if user is not None:
            login(request, user)
            if not Currency_Wallet.objects.filter(user = request.user).exists():
                add_wallet_detail(request.user)
            return redirect('/auth/verify/')
        return redirect('/auth/verify/')
        

class Mobile_Verfication(View):
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            phone = request.POST.get('phone')

            if phone!=None:

                user_obj = Custom_User.objects.get(email = request.session.get('email'), is_otp_verified = False)
                user_obj.phone = phone
                user_obj.save()
                otp_gen = random.randint(000000,999999)
                user_otp = User_OTP(user = user_obj, email = request.session.get('email'), otp = otp_gen)
                user_otp.save()
                send_otp(phone, otp_gen)
                return JsonResponse({'msg':'sent OTP successfully'})
            return JsonResponse({'msg':'Enter phone'})
        return redirect('/auth/verify')

class Verify_Mobile_OTP(View):
    def post(self, request, *args, **kwargs):
        email = request.session.get('email')
        mob_otp = request.POST.get('mob_otp')
        if mob_otp != None:
            otp_obj = User_OTP.objects.filter(user__email = email).last()
            if otp_obj.otp == int(mob_otp):
                otp_obj.user.is_otp_verified = True
                otp_obj.user.save()
                return redirect('/auth/verify')
            return redirect('/auth/verify')

        return redirect('/auth/verify')
     


class Verify_Otp(View):

    template_name = 'authentication/otpverify.html'

    def get(self, request, *args, **kwargs):

        return render(request, template_name = self.template_name)

    def post(self, request, *args, **kwargs):
        ist = request.POST.get('ist')
        sec = request.POST.get('sec')
        third = request.POST.get('third')
        fourth = request.POST.get('fourth')
        fifth = request.POST.get('fifth')
        sixth = request.POST.get('sixth')

        user_otp = ist+sec+third+fourth+fifth+sixth
        print(user_otp)
        if len(user_otp) == 6 :
            email = request.session.get('email')
            otp_obj = User_OTP.objects.get(user__email = email)
            if otp_obj.otp == int(user_otp):                                                      
                otp_obj.user.is_active = True
                otp_obj.user.save()
                return JsonResponse({'status': '200', 'url':'/auth/login'})
    
        return JsonResponse({'status': '400', 'msg':'Incorrect OTP',})


class Resend_Email(View):
    def get(self, request, *args, **kwargs):
        email = request.session.get('email') 
        user_obj = Custom_User.objects.get(email = email)
        send_email(user_obj)
        return redirect('/auth/verify/')


class Resend_Otp(View):
    def get(self, request, *args, **kwargs):
        email = request.session.get('email')
        user_obj = Custom_User.objects.get(email = email, is_active = False)
        otp_gen = random.randint(000000,999999)
        user_otp = User_OTP.objects.get(user = user_obj)
        user_otp.otp = otp_gen
        user_otp.save()
        send_html_email(email, otp_gen)
        
        return redirect('/auth/verifyotp')


def create_user_wallet(user):

    master_wallet = Wallet.deserialize(WALLET_PUBKEY)
    print(master_wallet, 'master wallet')
    user_wallet = master_wallet.create_new_address_for_user(user.id)
    print(user_wallet, 'user wallet')
    payment_address = user_wallet.to_address()
    print(payment_address, 'payment address')
    user_obj = Custom_User.objects.get(email = user.email)
    user_obj.user_wallet_address = payment_address
    user_obj.save()
    return None

def add_wallet_detail(user):
    private_key = random_key()
    public_key = privkey_to_pubkey(private_key)
    wallet_address = pubkey_to_address(public_key)

    
    coin_obj = CoinPair.objects.all()
    
    all_coins = [Currency_Wallet(user = user, coin_pair = i, public_key = public_key, available_bal = 0, wallet_address = wallet_address, locked_bal = 0, total_bal = 0, usdt_bal = 0) for i in coin_obj]
    Currency_Wallet.objects.bulk_create(all_coins)
    return None


class User_KYC_View(View):
    def post(self, request, *args, **kwargs):
                
        first_name = request.POST.get('first_name')
        mid_name = request.POST.get('mid_name')
        last_name = request.POST.get('last_name')
        dob = request.POST.get('dob')
        address = request.POST.get('address')
        city = request.POST.get('city')
        zipcode = request.POST.get('zipcode')

        try:
            email = request.user.email
        except Exception as e:
            try:
                email = request.session.get('email')
            except Exception as e1:
                return redirect('/auth/verify/')

        try:
            user_obj = Custom_User.objects.get(email = email, is_kyc_verified = False)
        except Exception as e:
            user_obj = Custom_User.objects.get(email = email, is_kyc_verified = True)

        user_obj.first_name = first_name
        user_obj.middle_name = mid_name
        user_obj.last_name = last_name
        # user_obj.dob = dob
        user_obj.address = address
        user_obj.city = city
        user_obj.zipcode = zipcode
        

        # KYC detail fetch
        kyc_id = request.POST.get('kyc_id')
        document_type = request.POST.get('document_type')
        confirm_kyc_id = request.POST.get('confirm_kyc_id')
        kyc_front_pic = request.FILES.get('kyc_front_pic')
        kyc_back_pic = request.FILES.get('kyc_back_pic')
        kyc_selfie = request.FILES.get('kyc_selfie')

        
        if kyc_id != confirm_kyc_id:
            return render(request, 'verification.html', {'kyc_id' : kyc_id, 'document_type' : document_type, 'confirm_kyc_id' : confirm_kyc_id, 'kyc_front_pic' : kyc_front_pic, 'kyc_back_pic' : kyc_back_pic, 'kyc_selfie' : kyc_selfie})

        if document_type == "red":
            document_type = "SSN"
        elif document_type == "yellow":
            document_type = "PASSPORT"
        else:
            document_type = "DRIVING_LICENSE"                                    
        kyc_obj = User_KYC.objects.create(user = user_obj, document_type = document_type, id_number = kyc_id, doc_front_img = kyc_front_pic, doc_back_img = kyc_back_pic, doc_selfie = kyc_selfie)
        if kyc_obj:
            user_obj.is_kyc_verified = True
            user_obj.save()
            create_user_wallet(user_obj)
            return redirect('/exchange')
        return render(request, 'verification.html', {'kyc_id' : kyc_id, 'document_type' : document_type, 'confirm_kyc_id' : confirm_kyc_id, 'kyc_front_pic' : kyc_front_pic, 'kyc_back_pic' : kyc_back_pic, 'kyc_selfie' : kyc_selfie})



class User_Login(View):

    template_name = 'authentication/login.html'

    def get(self, request, *args, **kwargs):                                                                                   

        return render(request, template_name = self.template_name)
    
    def post(self, request, *args, **kwargs):

        email = request.POST.get('email')
        password = request.POST.get('password')
        if email == "" or email == None or password == "" or password == None:
            messages.warning(request, 'Please enter full detail', 'danger')
            return redirect('/auth/login/')
        print(email, password)
        user = authenticate(email = email, password = password)
        print(user)
        if user is not None:
            login(request, user)
            if not Currency_Wallet.objects.filter(user = request.user).exists():
                add_wallet_detail(request.user)
                create_user_wallet(user)

            return redirect('/')

        messages.error(request, 'Wrong email or passsword', 'warning')

        return render(request, template_name = self.template_name)

class User_Logout(View):                        

    def post(self, request, *args, **kwargs):

        logout(request)

        return redirect('/auth/login')