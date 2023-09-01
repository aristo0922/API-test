import json
import time
from random import randint

import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from APIconnect.settings import get_secret
from .models import AuthUser
from .utils import make_signature


# Create your views here.
class AuthSmsSendView(APIView):
    def send_sms(self, phone_number, auth_number):
        timestamp = str(int(time.time() * 1000))

        headers={
            'Content-Type': 'application/json; charset=utf-8',
            'x-ncp-apigw-timestamp': timestamp,  # 네이버 API 서버와 5분이상 시간차이 발생시 오류
            'x-ncp-iam-access-key': f'{get_secret("SMS_ACCESS_KEY_ID")}',
            'x-ncp-apigw-signature-v2': make_signature(timestamp)  # utils.py 이용
        }

        body={
            'type':'SMS',
            'countryCode':'82',
            'contentType':'COMM',
            'from':f'{get_secret("SMS_SEND_PHONE_NUMBER")}',
            'messages':[{
                'to': phone_number,
            }],
            'content': f'아령 테스트 중... 진짜 못받음?? 인증번호[{auth_number}',
        }

        requests.post(get_secret("SMS_SEND_URI"), data=json.dumps(body), headers= headers)

    # 메시지 전달
    def post(self, request):
        try:
            input_data=json.loads(request.body)
            input_phone_number=input_data['phone_number']
            create_auth_number=randint(1000, 10000)
            self.send_sms(phone_number=input_phone_number, auth_number=create_auth_number)
            return Response({"message":"success"}, status=status.HTTP_200_OK)

        except:
            return Response({"message":"시스템 오류! 새로고침 후 다시 시도해 주세요."}, status=status.HTTP_401_UNAUTHORIZED)

class Identificate(APIView):
    # TODO: 사용자 인증 번호를 서버 내에서 저장할 수 있도록 db 수정
    def post(self, request):
        try:
            input_data=json.loads(request.body)
            user_input_number=input_data['user_input']
            auth_number=input_data['auth_number']

            if user_input_number == auth_number:
                AuthUser.objects.update_or_create(phone_number=input_data['phone_number'], is_valid=True)

            return Response({"message": "success"}, status=status.HTTP_201_CREATED)

        except:
            return Response({"message":"인증번호를 다시 확인해주세요"}, status=status.HTTP_401_UNAUTHORIZED)

class RegisterUser(APIView):
    # 회원가입
    def post(self, request):
        try:
            input_data=json.loads(request.body)
            user=AuthUser.objects.get(phone_number=input_data['phone_number'])
            if user:
                AuthUser.objects.update(phone_number=input_data['phone_number'], user_name=input_data['user_name'])
            else:
                return Response({"message":"전화번호 인증을 해주세요"}, status=status.HTTP_401_UNAUTHORIZED)
            return Response({"message":"success"}, status=status.HTTP_201_CREATED)

        except:
            return Response({"message": "다시 한번 시도해주세요!"}, status=status.HTTP_401_UNAUTHORIZED)

    def get(self, request):
        input_data=json.loads(request.body)
        user = AuthUser.objects.get(phone_number=input_data['phone_number'])

        response_data={"user_name": user.get_name(), "is_valid": user.get_valid()}

        return Response( response_data, status=status.HTTP_200_OK)
