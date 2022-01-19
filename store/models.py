from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import reverse



class Food(models.Model):
    name=models.CharField(max_length=200)
    price=models.DecimalField(decimal_places=2, max_digits=6)
    image=models.ImageField(null=True, blank=True)
    slug=models.SlugField()
    def __str__(self):
        return self.name

    @property
    def imageURL(self):
    	try:
    		url = self.image.url
    	except:
    		url = ''
    	return url

    def get_add_to_cart_url(self):
        return reverse("store:add-to-cart", kwargs={'slug': self.slug})

    def get_remove_from_cart_url(self):
        return reverse("store:remove-from-cart", kwargs={'slug': self.slug})




class OrderFood(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null= True)
    food=models.ForeignKey(Food, on_delete=models.SET_NULL, null= True)
    ordered=models.BooleanField(default=False)
    quantity=models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.food.name}"

    def get_total_food_price(self):
        return self.quantity * self.food.price


class Order(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null= True)
    paid=models.BooleanField(default=False)
    order_number=models.CharField(max_length=100)
    foods=models.ManyToManyField(OrderFood)
    ordered=models.BooleanField(default=False)
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, blank=True, null=True)


    def __str__(self):
        return str(self.user.username)

    def get_total(self):
        total=0
        for order_food in self.foods.all():
            total += order_food.get_total_food_price()
        return total

class Payment(models.Model):
    order_number = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
