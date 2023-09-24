from django.db import models
from ckeditor.fields import RichTextField

from pages.models import Office


class Car(models.Model):
    title = models.CharField(max_length=150)
    price = models.PositiveIntegerField(verbose_name="Price in $")
    description = RichTextField(max_length=1000)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    address = models.ManyToManyField(Office, related_name='cars_in_stock', blank=True, verbose_name="In stock at")
    main_photo = models.ImageField(upload_to='cars/%Y/%m/%d/', verbose_name='Main photo')
    photo_2 = models.ImageField(upload_to='cars/%Y/%m/%d/', blank=True, null=True)
    photo_3 = models.ImageField(upload_to='cars/%Y/%m/%d/', blank=True, null=True)
    photo_4 = models.ImageField(upload_to='cars/%Y/%m/%d/', blank=True, null=True)
    photo_5 = models.ImageField(upload_to='cars/%Y/%m/%d/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title


class CarAttribute(models.Model):
    name = models.CharField(max_length=100, unique=True)
    cars = models.ManyToManyField(Car, through='CarAttributeValue')

    def __str__(self) -> str:
        return self.name


class CarAttributeValue(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="attributes")
    attribute = models.ForeignKey(CarAttribute, on_delete=models.CASCADE)
    value = models.CharField(max_length=255)

    class Meta:
        unique_together = ['car', 'attribute']
        verbose_name = "Car attribute"
        verbose_name_plural = "Car attributes"

    def __str__(self) -> str:
        return ''


class CarFeature(models.Model):
    name = models.CharField(max_length=100, unique=True)
    cars = models.ManyToManyField(Car, through='CarFeatureAssociation', related_name="features")

    def __str__(self) -> str:
        return self.name


class CarFeatureAssociation(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    feature = models.ForeignKey(CarFeature, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['car', 'feature']
        verbose_name = "Car feature"
        verbose_name_plural = "Car features"

    def __str__(self) -> str:
        return ''
