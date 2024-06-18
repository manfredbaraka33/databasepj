from django.db import models

# Create your models here.

class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    room_number = models.CharField(max_length=10)
    image = models.ImageField(upload_to='student_profile_images/', null=True, blank=True,default='default.jpg')
    address = models.CharField(max_length=200, default='')
    password=models.CharField(max_length=100, default='')
    


    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Employee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    profile_image = models.ImageField(upload_to='employee_profile_images/', null=True, blank=True)
    password = models.CharField(default='xxxx')
    
    def __str__(self):
     return f"{self.first_name} {self.last_name}"
 
class MaintenanceIssue(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    reported_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(default='Reported')
    room_number = models.CharField(max_length=10,default=00)
    

    def __str__(self):
        return self.title