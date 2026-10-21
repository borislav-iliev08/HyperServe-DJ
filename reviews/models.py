from django.core.validators import MinLengthValidator
from django.db import models
from restaurants.models import Restaurant


# Create your models here.
class Review(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    author = models.CharField(max_length=50,validators=[MinLengthValidator(3,message='Authors\'s name must be at least 3 symbols long!')])
    created_at = models.DateTimeField(auto_now_add=True)
    restaurant = models.ForeignKey(Restaurant,on_delete=models.SET_NULL,blank=True,null=True,related_name='restaurant_reviews')
    is_flagged = models.BooleanField(default=False,editable=False)

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
