from django.db import models

# Create your models here.
class UserForm(models.Model):
    id = models.AutoField(primary_key=True)
    first_name =  models.TextField()
    last_name =  models.TextField()
    username =  models.TextField()
    email =  models.EmailField(unique=True)
    phone = models.TextField()
    city = models.TextField()
    address = models.TextField()
    password=models.TextField()
    profile=models.ImageField(upload_to='profile/', null=True, blank=True) 

    class Meta:
        managed = False
        db_table = 'sign_up'

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return self.name