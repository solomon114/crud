from django.db import models

# Create your models here.

class Employee(models.Model):  
    eid = models.CharField(max_length=20)  
    ename = models.CharField(max_length=100)  
    eemail = models.EmailField()  
    econtact = models.CharField(max_length=15)  
    eimage=models.ImageField(upload_to="emp", null=True)
    class Meta:  
        db_table = "employee"  