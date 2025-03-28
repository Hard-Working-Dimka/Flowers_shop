import io

from django.contrib.auth.models import AbstractUser
from django.db import models
from PIL import Image


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
    flowers = models.ManyToManyField(Flower, related_name='bouquets')
    events = models.ManyToManyField(Event, related_name='bouquets')
    color_palette = models.ManyToManyField(ColorPalette, blank=True, related_name='bouquets')
    binary_photo = models.BinaryField(null=True, blank=True, editable=True)

    def __str__(self):
        return f'{self.name} - {self.price}'

    def save(self, *args, **kwargs):
        try:
            image = Image.open(self.binary_photo)

            img_io = io.BytesIO()
            image.save(img_io, format=image.format)
            img_io.seek(0)

            self.binary_photo = img_io.read()
            super(BouquetOfFlowers, self).save(*args, **kwargs)
        except UnicodeDecodeError:
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
