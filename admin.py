from django.contrib import admin
from .models import Student,Employee,MaintenanceIssue
# Register your models here.
admin.site.register(Student)
admin.site.register(Employee)
admin.site.register(MaintenanceIssue)