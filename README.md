## send SMS with naver cloud
< <a href="https://www.ncloud.com/">official site</a> >
<br/><br/>

#### How to run?
1. set you secret key
```commandline
{
	"SECRET_KEY": "this line is for django secrets key",
	"SMS_ACCESS_KEY_ID": "your access key id.",
	"SMS_SERVICE_SECRET": "your access key secret password",
	"SMS_SEND_PHONE_NUMBER": "what number will you send message with",
	"SMS_PROJECT_ID": "you project id in naver console",
	"SMS_SEND_URI": "https://sens.apigw.ntruss.com/sms/v2/services/"+ here is you project id+"/messages",
	"SMS_SIGNATURE_URI": "/sms/v2/services/"+here is your project id+"/messages"
}
```

2. run this code
```
python manage.py makemigrations
python manage.py migrate

python manage.py runserver
```