from django.db import models
# Create your models here.
class Employee(models.Model):
    id=models.IntegerField(primary_key=True) 
    dept = models.CharField(max_length=20)  
    name = models.CharField(max_length=100)  
    email = models.EmailField()  
    location = models.CharField(max_length=15)
class Visitor(models.Model):
    id=models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)  
    email = models.EmailField()  
    phone=models.IntegerField()
    location = models.CharField(max_length=15)
    employee_name=models.CharField(max_length=15)
    status=models.CharField(max_length=18)
