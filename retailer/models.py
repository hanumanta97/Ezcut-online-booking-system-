from django.db import models

# Create your models here.
class buisness(models.Model):
    id = models.AutoField(primary_key=True)
    eamil_id =  models.TextField()
    buisness_name =  models.TextField()
    user_name =  models.EmailField()
    phone = models.TextField()
    city = models.TextField()
    services =  models.ImageField()
    services_price = models.TextField()
    shop_address = models.TextField()
    password_user=models.TextField()
    user_id=models.TextField()

    class Meta:
        managed = False
        db_table = 'buisness'

class review(models.Model):
    id = models.AutoField(primary_key=True)
    shop_id =  models.TextField()
    username =  models.EmailField()
    usermessage = models.TextField()
    rating = models.FloatField()

    class Meta:
        managed = False
        db_table = 'review'

class schedule(models.Model):
    id = models.AutoField(primary_key=True)
    shop_id =  models.TextField()
    user_id =  models.TextField()
    services =  models.EmailField()
    total_price = models.TextField()
    time = models.TimeField()
    date =  models.DateField()
    status = models.TextField()
    appointment_record=models.DateTimeField(auto_now=True)
    remarks = models.TextField()
  

    class Meta:
        managed = False
        db_table = 'schedule_appointment'
