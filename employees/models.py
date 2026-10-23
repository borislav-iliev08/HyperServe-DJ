from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from employees.validators import validate_real_domain
from restaurants.models import Restaurant
from reviews.models import Review


# Create your models here.

class Employee(models.Model):
    class PositionChoices(models.TextChoices):
        CH = 'Chef', 'Chef'
        SO = 'Sous Chef', 'Sous Chef'
        WA = 'Waiter', 'Waiter'
        BA = 'Bartender', 'Bartender'
        HO = 'Host', 'Host'
        MA = 'Manager', 'Manager'
        CL = 'Cleaner', 'Cleaner'
        CE = 'CEO','CEO'
        OT = 'Other', 'Other'
        
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True,validators=[validate_real_domain])
    phone_number = models.CharField(max_length=20,unique=True)
    profile_picture = models.ImageField(upload_to='employees/', blank=True, null=True)
    position = models.CharField(choices=PositionChoices.choices,max_length=20,default=PositionChoices.OT)
    restaurant = models.ForeignKey(Restaurant,on_delete=models.SET_NULL,blank=True,null=True)

    class Meta:
        verbose_name = "Employee"
        verbose_name_plural = "Employees"

class EmployeeReview(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='reviews')
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.DecimalField(max_digits=4,decimal_places=2)
    author = models.CharField(max_length=50)
    is_flagged = models.BooleanField(default=False,editable=False)

    class Meta:
        verbose_name = "Employee Review"
        verbose_name_plural = "Employee Reviews"

