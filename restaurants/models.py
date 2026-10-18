from django.db import models
from django.utils.text import slugify


# Create your models here.
class Perks(models.Model):
    name = models.CharField(max_length=50,unique=True)


class Restaurant(models.Model):
    class TypeChoices(models.TextChoices):
        JA = 'Japanese','Japanese'
        BU = 'Bulgarian','Bulgarian'
        AM = 'American','American'
        IT = 'Italian','Italian'
        IN = 'Indonesian','Indonesian'
        SP = 'Spanish','Spanish'
        OT = 'Other','Other'
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    description = models.TextField(blank=True,null=True)
    cuisine_type = models.CharField(choices=TypeChoices.choices,default=TypeChoices.OT,max_length=30)
    perks = models.ManyToManyField(Perks,blank=True,related_name='restaurant_perks')
    owner = models.CharField(max_length=50)
    rating = models.PositiveIntegerField()
    slug = models.CharField(max_length=50,blank=True,null=True)

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug =slugify(f'{self.name} {self.cuisine_type}')
        super().save(*args,**kwargs)





