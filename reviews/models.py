from django.db import models
from restaurants.models import Restaurant


# Create your models here.
class Review(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    author = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    restaurant = models.ForeignKey(Restaurant,on_delete=models.SET_NULL,blank=True,null=True,related_name='restaurant_reviews')

