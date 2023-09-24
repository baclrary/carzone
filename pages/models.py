from django.db import models

from .validators import validate_phone


class Team(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    designation = models.ForeignKey("Office", related_name='office_staff', on_delete=models.SET_NULL, 
                                    null=True, blank=True)
    photo = models.ImageField(upload_to='staff/%Y/%m/%d/')
    facebook_link = models.URLField(max_length=200)
    twitter_link = models.URLField(max_length=200)
    instagram_link = models.URLField(max_length=200)
    created_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
    
class Office(models.Model):
    name = models.CharField(max_length=300)
    street = models.CharField(max_length=300)
    city = models.CharField(max_length=300)
    state = models.CharField(max_length=300)
    country = models.CharField(max_length=300)
    phone = models.CharField(max_length=20, unique=True, blank=True, null=True, validators=[validate_phone])
    email = models.EmailField(unique=True)
    main_photo = models.ImageField(upload_to='offices//%Y/%m/%d/')
    photo_2 = models.ImageField(upload_to='offices//%Y/%m/%d/', blank=True, null=True)
    photo_3 = models.ImageField(upload_to='offices//%Y/%m/%d/', blank=True, null=True)
    photo_4 = models.ImageField(upload_to='offices//%Y/%m/%d/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.name
    
    def get_address(self) -> str:
        return f"{self.street}, {self.city}, {self.state} - {self.country}"
    
class OfficeHours(models.Model):
    DAY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]
    HOUR_CHOICES = [(str(i), "{:02d}".format(i)) for i in range(24)]
    MINUTE_CHOICES = [(str(i), "{:02d}".format(i)) for i in range(0, 60, 5)]

    office = models.ForeignKey(Office, on_delete=models.CASCADE, related_name='hours')
    day = models.CharField(choices=DAY_CHOICES, max_length=10)
    
    open_hour = models.CharField(choices=HOUR_CHOICES, max_length=2)
    open_minute = models.CharField(choices=MINUTE_CHOICES, max_length=2)
    
    close_hour = models.CharField(choices=HOUR_CHOICES, max_length=2)
    close_minute = models.CharField(choices=MINUTE_CHOICES, max_length=2)

    class Meta:
        unique_together = ['office', 'day']
        
    def __str__(self):
        return ''

    def get_open_time(self):
        return "{}:{}".format(self.open_hour, self.open_minute)

    def get_close_time(self):
        return "{}:{}".format(self.close_hour, self.close_minute)
