from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    telegram_id = models.BigIntegerField(unique=True, blank=True, null=True)
    telegram_username = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.username} - {self.telegram_username}"


class Flower(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class BouquetOfFlowers(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=10)
    photo = models.ImageField(null=True, blank=True, upload_to='photos_of_bouquets')
    flowers = models.ManyToManyField(Flower)
    events = models.ManyToManyField(Event)

    def __str__(self):
        return self.name


class Consultation(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='consultations')
    created = models.DateTimeField(auto_now_add=True)
    question = models.TextField(null=True, blank=True)
    phone_number = models.BigIntegerField()
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.customer


class Order(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders')
    address = models.CharField(max_length=50)
    status = models.BooleanField(default=False)
    BouquetOfFlowers = models.ForeignKey(BouquetOfFlowers, on_delete=models.CASCADE, related_name='orders')
    delivery = models.DateTimeField()
    phone_number = models.BigIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True, null=True)
    total_price = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return self.customer
