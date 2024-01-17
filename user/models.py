from django.db import models
from django.contrib.auth.models import User
from food.models import *

# Create your models here.
class OrderHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    order_price = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    food_price = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)