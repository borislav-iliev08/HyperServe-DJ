from django.db import models
from django.utils.text import slugify
from restaurants.validators import validate_real_domain


# Create your models here.
class Perks(models.Model):
    name = models.CharField(max_length=50,unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Perk"
        verbose_name_plural = "Perks"

class Restaurant(models.Model):
    class TypeChoices(models.TextChoices):
        JA = 'Japanese','Japanese'
        BU = 'Bulgarian','Bulgarian'
        AM = 'American','American'
        IT = 'Italian','Italian'
        IN = 'Indonesian','Indonesian'
        SP = 'Spanish','Spanish'
        OT = 'Other','Other'
    name = models.CharField(max_length=50,unique=True)
    address = models.CharField(max_length=200,unique=True)
    email = models.EmailField(unique=True,validators=[validate_real_domain])
    image = models.ImageField(upload_to='restaurants/', blank=True, null=True)
    description = models.TextField(blank=True,null=True)
    cuisine_type = models.CharField(choices=TypeChoices.choices,default=TypeChoices.OT,max_length=30)
    perks = models.ManyToManyField(Perks,blank=True,related_name='restaurant_perks')
    owner = models.CharField(max_length=50)
    rating = models.PositiveIntegerField(default=0, editable=False)
    slug = models.CharField(max_length=100,blank=True)


    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug =slugify(f'{self.name} {self.cuisine_type}')
        super().save(*args,**kwargs)

    class Meta:
        verbose_name = "Restaurant"
        verbose_name_plural = "Restaurants"




