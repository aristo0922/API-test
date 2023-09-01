from django.db import models

# Create your models here.
class AuthUser(models.Model):
    phone_number=models.CharField(max_length=11, primary_key=True)
    user_name = models.CharField(max_length=10)
    is_valid= models.BooleanField(default=False)
    class Meta:
        db_table='User'

    def get_name(self):
        return self.user_name

    def get_valid(self):
        return self.is_valid
