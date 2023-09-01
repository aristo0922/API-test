import hashlib
import hmac
import base64

from APIconnect.settings import get_secret


def make_signature(timestamp):
    access_key = get_secret("SMS_ACCESS_KEY_ID")
    secret_key = get_secret("SMS_SERVICE_SECRET")
    secret_key = bytes(secret_key, 'UTF-8')

    uri = get_secret("SMS_SEND_URI")
    # uri 중간에 Console - Project - 해당 Project 서비스 ID 입력 (예시 = ncp:sms:kr:263092132141:sms)

    message = "POST" + " " + uri + "\n" + timestamp + "\n" + access_key
    message = bytes(message, 'UTF-8')
    signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
    return signingKey
