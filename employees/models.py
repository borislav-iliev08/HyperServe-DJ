from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from restaurants.models import Restaurant
from reviews.models import Review


# Create your models here.

class Employee(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20,unique=True)
    profile_picture = models.ImageField(upload_to='employees/', blank=True, null=True)
    position = models.CharField(max_length=20)
    restaurant = models.ForeignKey(Restaurant,on_delete=models.SET_NULL,blank=True,null=True)

class EmployeeReview(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='reviews')
    title = models.CharField(max_length=100)
    content = models.TextField()
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(6)])
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=50)
