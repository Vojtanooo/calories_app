# Generated by Django 3.2.8 on 2021-10-13 08:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('counter', '0002_caloriesperday'),
    ]

    operations = [
        migrations.AlterField(
            model_name='caloriesperday',
            name='day',
            field=models.DateField(default=datetime.date(2021, 10, 13)),
        ),
    ]