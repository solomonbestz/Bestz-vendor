from django.db import models
from django.conf import settings
# Create your models here.
import secrets

class Category(models.Model):
    title=models.CharField(max_length=25)

    def __str__(self):
        return self.title


class Item(models.Model):
    vendor=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete= models.CASCADE,null=True)
    title=models.CharField(max_length=25)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    delivery_fee=models.FloatField(default=0)
    different_location_fee=models.FloatField(default=0)
    delivery_date=models.CharField(max_length=40,null=True,blank=True)
    price=models.FloatField()

    def __str__(self):
        return self.title


class OrderItem(models.Model):
    vendor=models.ForeignKey(settings.AUTH_USER_MODEL,related_name="vendor",on_delete= models.CASCADE)
    item=models.ForeignKey(Item,on_delete=models.CASCADE,null=True)
    is_ordered=models.BooleanField(default=False)
    is_removed=models.BooleanField(default=False)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete= models.CASCADE,related_name="user",null=True)
    delivery_location=models.CharField(max_length=40,null=True,blank=True)
    quantity=models.IntegerField(default=1)

    def __str__(self):
        return self.item.title

    def get_total_item_price(self,delivery_location):
        if delivery_location == self.vendor.university:
            return self.quantity * (self.item.price+ self.item.delivery_fee)

        else:
            return self.quantity * (self.item.price + self.item.different_location_fee)


class Order(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete= models.CASCADE)
    items=models.ManyToManyField(OrderItem)
    is_ordered=models.BooleanField(default=False)
    start_date=models.DateTimeField(auto_now_add=True)
    ref=models.CharField(max_length=200,null=True,blank=True)
    delivery_location=models.CharField(max_length=40,null=True,blank=True)

    def __str__(self):
        return self.user.fullname

    def get_total(self):
        total=0
        for order_item in self.items.all():
            total+=order_item.get_total_item_price(self.delivery_location)

        return total


class Payment(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete= models.CASCADE)
    amount=models.PositiveIntegerField()
    email=models.EmailField()
    ref=models.CharField(max_length=200)
    verified=models.BooleanField(default=False)
    date_created=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=('-date_created',)

    def __str__(self):
        return str(self.amount)

    def save(self,*args,**kwargs):
        while not self.ref:
            ref=secrets.token_urlsafe(50)
            obj_with_similar_ref=Payment.objects.filter(ref=ref)
            if not obj_with_similar_ref:
                self.ref=ref


        super().save(*args,**kwargs)

    def amount_value(self):
        return self.amount * 100
