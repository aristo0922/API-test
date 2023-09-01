from django.urls import path

from naverSMS.views import AuthSmsSendView, RegisterUser, Identificate

urlpatterns=[
    path('sms/send/', AuthSmsSendView.as_view(), name="send_SMS"),
    path('sms/auth/', Identificate.as_view(), name="identification"),
    path('register/', RegisterUser.as_view(), name="SignUp"),

]