from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    fullName = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phoneNumber = models.CharField(max_length=10)
    adress = models.TextField()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

class Supplier(models.Model):
    email = models.EmailField()
    phoneNumber = models.CharField(max_length=10)
    actualAdress = models.TextField()
    nameSupplier = models.CharField(max_length=70)

class Supply(models.Model):
    supplyNumber = models.IntegerField()
    dateSupply = models.DateField()
    idSupplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)

class Manafacturer(models.Model):
    name = models.CharField(max_length=50)
    country = models.CharField(max_length=50)

class ProductType(models.Model):
    typeName = models.CharField(max_length=70,default="Смартфон")

class Product(models.Model):
    article = models.IntegerField()
    productType = models.ForeignKey(ProductType,on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    price = models.FloatField()
    count = models.IntegerField()
    photoLink = models.CharField(max_length=100,default="127.0.0.1")
    idSupply = models.ForeignKey(Supply, on_delete=models.CASCADE)
    isAdvertisement = models.BooleanField()
    idManafacturer = models.ForeignKey(Manafacturer, on_delete=models.CASCADE)

class Purchases(models.Model):
    idUser = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    idProduct = models.ForeignKey(Product, on_delete=models.CASCADE)
    datePurchase= models.DateField()
    orderStage = models.CharField(max_length=50,default="Оплачен")

class Specifications(models.Model):
    shortSpecification = models.CharField(max_length=1000)
    fullSpecification = models.CharField(max_length=1000)
    idProduct = models.ForeignKey(Product, on_delete=models.CASCADE)

class Basket(models.Model):
    idUser = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    idProduct = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField()