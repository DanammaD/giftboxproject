from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    CAT=((1,'Cake'),(2,'Chocolates'),(3,'flowerpot'),(4,'Personlisedgift'),(5,'Plants'),(6,'Perfumes'),(7,'Combos'))
    name=models.CharField(max_length=50,verbose_name='Product Name')
    price=models.FloatField()
    pdetails=models.CharField(max_length=200,verbose_name='Product details')
    cat=models.IntegerField(verbose_name='Category',choices=CAT)
    is_active=models.BooleanField(default=True,verbose_name='Availbale')
    pimage=models.ImageField(upload_to='image')

class Cart(models.Model):
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")
    pid=models.ForeignKey(Product,on_delete=models.CASCADE,db_column="pid")
    qty=models.IntegerField(default=1)

class Order(models.Model):
   order_id=models.CharField(max_length=50)
   uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")
   pid=models.ForeignKey(Product,on_delete=models.CASCADE,db_column="pid")
   qty=models.IntegerField(default=1)