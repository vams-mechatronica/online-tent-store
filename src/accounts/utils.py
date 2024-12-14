
from django.conf import settings
from django.http import JsonResponse
from .models import DeviceOtp, Country
from django.http import JsonResponse
from datetime import date
from django.contrib import auth
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
import requests
from .serializers import UserSerializer
from django.contrib.auth import authenticate, get_user_model
# from infobip_channels.whatsapp.channel import WhatsAppChannel
import uuid
from random import randint as rand
# c = WhatsAppChannel.from_auth_params({
#     "base_url": settings.IB_BASE_URL,
#     "api_key": settings.IB_API_KEY
# })
user_model = get_user_model()


class OTPManager:
    @staticmethod
    def send_otp(fake_otp, otp, country_code, phone_number):
        count = DeviceOtp.objects.filter(
            number=phone_number, created_date__date=date.today()).count()
        
        if count > 5:
            return False
        
        try:
            device_otps = DeviceOtp.objects.filter(
                number=phone_number, status=True)
            for device_otp in device_otps:
                device_otp.status = False
                device_otp.save()
        except Exception as e:
            print(e)
            pass

        country_code = country_code.replace('+', '').strip()

        country, _ = Country.objects.get_or_create(
            country_code=int(country_code))
        # if not fake_otp:
        #     response = c.send_text_message(
        #                 {
        #                 "from": str(settings.SENDER_PHONE_NUMBER),
        #                 "to": str(country_code+phone_number),
        #                 "messageId": str(uuid.uuid1),
        #                 "content": {
        #                     "text": f"Hi, Your VAMSCentral One-Time Password is {otp}. Please don't share this with anyone else. Regards, VAMSCentral"
        #                 },
                        
        #                 }
        #     )
        #     if response.status_code == 200:
        #         print(response )
        #         print('sent')
        #     msgtxt = str(otp) + ' is the OTP for Glovo Food Delivery App.'
        #     msgtxt = msgtxt.replace(" ", "%20")
            # url = "https://9rd3vd.api.infobip.com/sms/1/text/query?username=MudStudio&password=Prune@2022&from=IPrune&to=91" + \
            #     phone_number+"&indiaDltContentTemplateId=1107161513294569922&indiaDltPrincipalEntityId=1101439040000040339&text="+msgtxt
            # x = requests.get(url)
        DeviceOtp.objects.create(
            number=phone_number, otp=otp, status=True, country=country)
        return True

    @staticmethod
    def verify_otp(otp, country_code, phone_number,web):
        country_code = country_code.replace('+', '')
        country = Country.objects.get(country_code=country_code)
        device_otp = DeviceOtp.objects.get(
            number=phone_number, status=True, country=country)
        if int(otp) != device_otp.otp:
            return JsonResponse({'Error': "OTP Didn't matched!"}, status=status.HTTP_401_UNAUTHORIZED)
        user, created = user_model.objects.get_or_create(mobileno=phone_number)
        token, created = Token.objects.get_or_create(user=user)
        if web == False:
            device_otp.status = False
            device_otp.save()
            return JsonResponse({'user': UserSerializer(user).data, 'token': token.key},status=status.HTTP_201_CREATED)
        else:
            device_otp.status = False
            device_otp.save()
            return user
    