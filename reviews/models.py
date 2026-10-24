from django.core.validators import MaxValueValidator, MinLengthValidator, MinValueValidator
from django.db import models

from restaurants.models import Restaurant


# Create your models here.
class Review(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    author = models.CharField(max_length=50,validators=[MinLengthValidator(3,message='Authors\'s name must be at least 3 symbols long!')])
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.DecimalField(max_digits=4, decimal_places=2, validators=[MinValueValidator(1), MaxValueValidator(5)])
    restaurant = models.ForeignKey(Restaurant,on_delete=models.SET_NULL,blank=True,null=True,related_name='restaurant_reviews')
    is_flagged = models.BooleanField(default=False,editable=False)

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"


class EmployeeReview(models.Model):
    employee = models.ForeignKey('employees.Employee', on_delete=models.CASCADE, related_name='reviews')
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.DecimalField(max_digits=4,decimal_places=2,blank=True,null=True)
    author = models.CharField(max_length=50)
    is_flagged = models.BooleanField(default=False,editable=False)

    class Meta:
        verbose_name = "Employee Review"
        verbose_name_plural = "Employee Reviews"