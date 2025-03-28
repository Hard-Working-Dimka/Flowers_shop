# Generated by Django 5.1.7 on 2025-03-26 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flowers', '0004_alter_order_exclude_flowers'),
    ]

    operations = [
        migrations.CreateModel(
            name='ColorPalette',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='bouquetofflowers',
            name='color_palette',
            field=models.ManyToManyField(blank=True, related_name='bouquets', to='flowers.colorpalette'),
        ),
    ]
