from django.contrib import messages
from django.shortcuts import render,redirect
from django.contrib.auth.hashers import make_password, check_password
from .models import Student,MaintenanceIssue,Employee
from django.shortcuts import get_object_or_404

def hostel_view(request):
    return render(request, 'hostelMS/index.html')

def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        room_number = request.POST.get('room_number')
        address = request.POST.get('address')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        image = request.FILES.get('image') 
        
        if password != password2:
            messages.error(request, 'Passwords do not match')
            return render(request, 'hostelMS/register.html')

       
        if Student.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return render(request, 'appointment/register.html')
        if Student.objects.filter(phone_number=phone_number).exists():
            messages.error(request, 'Phone number already exists')
            return render(request, 'hostelMS/register.html')
        
     
        hashed_password = make_password(password)

        student = Student(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            room_number=room_number,
            address=address,
            password=hashed_password,
            image=image
        )
        student.save()   
        messages.success(request, 'Registration successful')
        return redirect('hostelMS:login') 
    return render(request,'hostelMS/register.html')

def prelogin(request):
    return render(request,'hostelMS/prelogin.html')


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            student = Student.objects.get(email=email)
            if check_password(password, student.password):
                request.session['student_id'] = student.id
                request.session.save() 
                messages.success(request, 'Login successful')
                return redirect('hostelMS:studentDb') 
            else:
                messages.error(request, 'Invalid password')
        except Student.DoesNotExist:
            messages.error(request, 'Invalid email')
    
    return render(request, 'hostelMS/login.html')



def login2(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            employee = Employee.objects.get(email=email)
            if password == employee.password:
                request.session['employee_id'] = employee.id
                request.session.save() 
                messages.success(request, 'Login successful')
                return redirect('hostelMS:employeeDb') 
            else:
                messages.error(request, 'Invalid password')
        except Employee.DoesNotExist:
            messages.error(request, 'Invalid email')
    
    return render(request, 'hostelMS/login2.html')

def studentDb(request):
    student_id = request.session.get('student_id')
    if not student_id:
        messages.error(request, 'You need to login first')
        return redirect('hostelMS:login2')
    student = Student.objects.get(id=student_id)
    listreported = MaintenanceIssue.objects.filter(student=student)
    listapproved = MaintenanceIssue.objects.filter(student=student,status='Approved')
    reported = MaintenanceIssue.objects.filter(student=student).count()
    approved = MaintenanceIssue.objects.filter(student=student,status='Approved').count()
    
    return render(request,'hostelMS/studentDb.html',{'student':student,
                                                     'listreported':listreported,
                                                     'reported':reported,
                                                     'listapproved':listapproved,
                                                     'approved':approved,
                                                     })

def employeeDb(request):
    student_id = request.session.get('student_id')
    student = Student.objects.get(id=student_id)
    employee_id = request.session.get('employee_id')
    if not employee_id:
        messages.error(request, 'You need to login first')
        return redirect('hostelMS:login2')
    employee = Employee.objects.get(id=employee_id)
    listreported = MaintenanceIssue.objects.all()
    reported = MaintenanceIssue.objects.all().count()
    students=Student.objects.all()
    studentsCount=students.count()
    
    return render(request,'hostelMS/employeeDb.html',{'employee':employee,
                                                      'listreported':listreported,
                                                      'reported':reported,
                                                      'students':students,
                                                      'studentsCount':studentsCount,
                                                      'student':student,
                                                      })


def issue(request):
    if request.method == 'POST':
        room_number = request.POST.get('room_number')
        title = request.POST.get('title')
        description = request.POST.get('description')
        
        student_id = request.session.get('student_id')
        
        maintainanceIssue = MaintenanceIssue(
            student_id=student_id,
            title=title,
            description = description,
            room_number=room_number,
        )
        
        maintainanceIssue.save()   
        messages.success(request, 'Maintainance Issue reported successfully')
        return redirect('hostelMS:studentDb')
    else:
        return render(request,'hostelMS/maintainance-report.html')
    
    
    
def account(request):
    student_id = request.session.get('student_id')
    student = Student.objects.get(id=student_id)
    return render(request, 'hostelMS/account.html', {'student':student})


def account2(request):
    employee_id = request.session.get('employee_id')
    employee = Employee.objects.get(id=employee_id)
    return render(request, 'hostelMS/account2.html', {'employee':employee})

def approve(request, maintainanceissue_id):
    maintainanceissue = get_object_or_404(MaintenanceIssue, id=maintainanceissue_id)
    
    if request.method == 'POST':
        maintainanceissue.status='Approved'
        maintainanceissue.save()
        messages.success(request, 'Maintainance issue approved successfully')
        return redirect('hostelMS:issuelist')  
    return render(request, 'hostelMS/approve_issue.html', {'maintainanceissue': maintainanceissue})

def issuelist(request):
    student_id = request.session.get('student_id')
    student = Student.objects.get(id=student_id)
    employee_id = request.session.get('employee_id')
    employee = Employee.objects.get(id=employee_id)
    maintenanceIssue = MaintenanceIssue.objects.filter()
    repoCount=maintenanceIssue.count()
    return render(request, 'hostelMS/issuelist.html', {'employee':employee,'student': student, 'issues': maintenanceIssue,'repoCount':repoCount})
      