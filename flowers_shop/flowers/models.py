import io

from django.contrib.auth.models import AbstractUser
from django.db import models

from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
import sys


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


class ColorPalette(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class BouquetOfFlowers(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=10)
    photo = models.ImageField(null=True, blank=False)
    flowers = models.ManyToManyField(Flower, related_name='bouquets')
    events = models.ManyToManyField(Event, related_name='bouquets')
    color_palette = models.ManyToManyField(ColorPalette, blank=True, related_name='bouquets')
    byte_photo = models.BinaryField(null=True, blank=True)

    def __str__(self):
        return f'{self.name} - {self.price}'

    def save(self, *args, **kwargs):
        image = Image.open(self.photo).convert('RGB')

        img_io = io.BytesIO()
        image.save(img_io, format='JPEG')  # Можно изменить формат на нужный (например, PNG)
        img_io.seek(0)

        self.byte_photo = img_io.read()
        self.photo = None
        super(BouquetOfFlowers, self).save(*args, **kwargs)


class Consultation(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='consultations')
    created = models.DateTimeField(auto_now_add=True)
    question = models.TextField(null=True, blank=True)
    phone_number = models.BigIntegerField()
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.customer.telegram_username


class Order(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders')
    address = models.CharField(max_length=50)
    status = models.BooleanField(default=False)
    bouquet_of_flowers = models.ForeignKey(BouquetOfFlowers, on_delete=models.CASCADE, related_name='orders')
    exclude_flowers = models.ManyToManyField(Flower, blank=True, related_name='orders')
    delivery = models.DateTimeField()
    phone_number = models.BigIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True, null=True)
    total_price = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return self.customer.telegram_username
