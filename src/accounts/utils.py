
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
import logging
logger = logging.getLogger(__name__)


class OTPManager:
    @staticmethod
    def send_otp(fake_otp, otp, country_code, phone_number):
        count = DeviceOtp.objects.filter(
            number=phone_number, created_date__date=date.today()).count()
        
        if count > 50:
            return False, count
        
        try:
            device_otps = DeviceOtp.objects.filter(
                number=phone_number, status=True)
            for device_otp in device_otps:
                device_otp.status = False
                device_otp.save()
        except Exception as e:
            logger.exception(e)

        country_code = country_code.replace('+', '').strip()

        country, _ = Country.objects.get_or_create(
            country_code=int(country_code))
        if not fake_otp:
            payload = {
                "messages": [
                    {
                    "from": "12248140388",
                    "to": country_code+phone_number,
                    "messageId": str(uuid.uuid1),
                    "content": {
                        "templateName": "otp_auth_wa",
                        "templateData": {
                        "body": {
                            "placeholders": [
                            str(otp)
                            ]
                        },
                        "buttons": [
                            {
                            "type": "URL",
                            "parameter": str(otp)
                            }
                        ]
                        },
                        "language": "en_GB"
                    },
                    "callbackData": "Callback data",
                    "notifyUrl": "https://ashekhar.pythonanywhere.com/marketing/whatsapp/delivery-status/add"
                    }
                ]
            }
            headers = {
                'Authorization': f"App {settings.INFOBIP_API_KEY}",
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            response = requests.post(settings.INFOBIP_SEND_TEMPLATE_MESSAGE_API_URL, json=payload, headers=headers)
            if response.status_code == 200:
                logger.info('Message Sent Successfully')
        DeviceOtp.objects.create(
            number=phone_number, otp=otp, status=True, country=country)
        return True, count

    @staticmethod
    def verify_otp(otp, country_code, phone_number,web):
        try:
            country_code = country_code.replace('+', '')
            country = Country.objects.get(country_code=country_code)
            try:
                device_otp = DeviceOtp.objects.get(
                    number=phone_number, status=True, country=country)
            except DeviceOtp.DoesNotExist:
                return Response({'Error':"OTP Didn't matched!"},status=status.HTTP_401_UNAUTHORIZED)
            if int(otp) != device_otp.otp:
                return JsonResponse({'Error': "OTP Didn't matched!"}, status=status.HTTP_401_UNAUTHORIZED)
            user, created = user_model.objects.get_or_create(mobileno=phone_number,is_mobileverified=True)
            token, created = Token.objects.get_or_create(user=user)
            if web == False:
                device_otp.status = False
                device_otp.save()
                return JsonResponse({'user': UserSerializer(user).data, 'token': token.key},status=status.HTTP_201_CREATED)
            else:
                device_otp.status = False
                device_otp.save()
                return user
        except Exception as err:
            logger.error(f'Error Occurred: {str(err)}')
    
    @staticmethod
    def verify_otp_for_seller(otp, country_code, phone_number,web):
        try:
            country_code = country_code.replace('+', '')
            country = Country.objects.get(country_code=country_code)
            try:
                device_otp = DeviceOtp.objects.get(
                    number=phone_number, status=True, country=country)
            except DeviceOtp.DoesNotExist:
                return Response({'Error':"OTP Didn't matched!"},status=status.HTTP_401_UNAUTHORIZED)
            if int(otp) != device_otp.otp:
                return JsonResponse({'Error': "OTP Didn't matched!"}, status=status.HTTP_401_UNAUTHORIZED)
            
            user, created = user_model.objects.get_or_create(mobileno=phone_number,role='supplier',is_supplier=True,is_mobileverified=True)
            token, created = Token.objects.get_or_create(user=user)
            
            if web == False:
                device_otp.status = False
                device_otp.save()
                return JsonResponse({'user': UserSerializer(user).data, 'token': token.key},status=status.HTTP_201_CREATED)
            else:
                device_otp.status = False
                device_otp.save()
                return user
        except Exception as err:
            logger.error(f'Error Occurred: {str(err)}')
    
    @staticmethod
    def verify_otp_for_bda_or_bde(otp, country_code, phone_number,web):
        try:
            country_code = country_code.replace('+', '')
            country = Country.objects.get(country_code=country_code)
            try:
                device_otp = DeviceOtp.objects.get(
                    number=phone_number, status=True, country=country)
            except DeviceOtp.DoesNotExist:
                return Response({'Error':"OTP Didn't matched!"},status=status.HTTP_401_UNAUTHORIZED)
            if int(otp) != device_otp.otp:
                return JsonResponse({'Error': "OTP Didn't matched!"}, status=status.HTTP_401_UNAUTHORIZED)
            
            user, created = user_model.objects.get_or_create(mobileno=phone_number,role='bde',is_supplier=True,is_mobileverified=True)
            token, created = Token.objects.get_or_create(user=user)
            
            if web == False:
                device_otp.status = False
                device_otp.save()
                return JsonResponse({'user': UserSerializer(user).data, 'token': token.key},status=status.HTTP_201_CREATED)
            else:
                device_otp.status = False
                device_otp.save()
                return user
        except Exception as err:
            logger.error(f'Error Occurred: {str(err)}')
    