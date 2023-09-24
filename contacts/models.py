from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Contact(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    car_id = models.IntegerField(blank=True)
    car_title = models.CharField(max_length=300)
    customer_need = models.CharField(max_length=300)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    email = models.EmailField()
    phone = PhoneNumberField(blank=True)
    message = models.TextField(max_length=2000)
    user_id = models.IntegerField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email} - {self.customer_need}"
