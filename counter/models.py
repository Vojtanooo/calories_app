from django.db import models
from datetime import date
from django.db.models.deletion import CASCADE

class User(models.Model):
    name = models.CharField(unique=True, max_length=50, primary_key=True)
    weight = models.IntegerField()
    height = models.IntegerField()
    age = models.IntegerField()
    gender = models.CharField(max_length=20)
    activity = models.CharField(max_length=200)
    bmr = models.IntegerField()

    def __str__(self):
        return self.name

class CaloriesPerDay(models.Model):
    user_name = models.ForeignKey(User, on_delete=CASCADE)
    day = models.DateField(default=date.today())
    day_bmr = models.IntegerField()

    def __str__(self):
        return f"{self.user_name}-{self.day}"
