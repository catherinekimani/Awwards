# Generated by Django 4.0.5 on 2022-06-15 19:25

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('awwardsapp', '0002_rating_average_rate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='average_rate',
            field=models.IntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)]),
        ),
    ]
