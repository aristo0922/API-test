import json
from random import randint

from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from APIconnect.settings import get_secret
from .models import AuthUser


# Create your views here.
class AuthSmsSendView(APIView):
    def send_sms(self, phone_number, auth_number):
        headers={
            'Content-Type': 'application/json; charset=utf-8',
            'x-ncp-auth-key': f'{get_secret("SMS_ACCESS_KEY_ID")}',
            'x-ncp-service-secret': f'{get_secret("SMS_SERVICE_SECRET")}',
        }

        data={
            'type':'SMS',
            'contentType':'COMM',
            'countryCode':'82',
            'from':f'{get_secret("SMS_SEND_PHONE_NUMBER")}',
            'to':[
                f'{get_secret("phone_number")}'
            ],
            'content':f'아령 테스트 중... 혹사 네 전화번호 써도 됨? 인증번호[{auth_number}'
        }
    # 메시지 전달
    def post(self, request):
        try:
            print(">>> input loads ")
            input_data=json.loads(request.body)
            print(">>> input phone number ")
            input_phone_number=input_data['phone_number']
            print(">>> input randint ")
            create_auth_number=randint(1000, 10000)
            print(">>> send_sms ")
            self.send_sms(phone_number=input_phone_number, auth_number=create_auth_number)
            return Response({"message":"success"}, status=status.HTTP_200_OK)

        except:
            return Response({"message":"failed!"}, status=status.HTTP_401_UNAUTHORIZED)

class Identificate(APIView):
    def post(self, request):
        try:
            input_data=json.loads(request.body)
            user_input_number=input_data['user_input']
            auth_number=input_data['auth_number']

            if user_input_number == auth_number:
                AuthUser.objects.update_or_create(phone_number=input_data['phone_number'], is_valid=True)
                AuthUser.save()

        except:
            return Response({"message":"인증번호를 다시 확인해주세요"}, status=status.HTTP_401_UNAUTHORIZED)

class RegisterUser(APIView):
    # 회원가입
    def post(self, request):
        try:
            input_data=json.loads(request.body)

            AuthUser.objects.update_or_create(phone_number=input_data['phone_number'], user_name=input_data['user_name'])
            AuthUser.save()
            return Response({"message":"success"}, status=status.HTTP_201_CREATED)

        except:
            return Response({"message": "failed!"}, status=status.HTTP_401_UNAUTHORIZED)

