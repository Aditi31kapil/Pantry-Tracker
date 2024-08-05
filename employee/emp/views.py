from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Employee, Role ,Department
from datetime import datetime
from django.db.models import Q
# Create your views here.
def index(request):
    return render(request,'index.html')

def all_emp(request):
    emps = Employee.objects.all()
    context = {
        'emps':emps
    }
    return render(request,'all_emp.html',context)

def add_emp(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        salary = request.POST['salary']
        bonus = request.POST['bonus']
        phone = request.POST['phone']
        role_id = request.POST['role']
        dept_id = request.POST['dept']
        hire_date_str = request.POST['hire_date']
        
        # Convert the hire_date_str to a datetime object
        try:
            hire_date = datetime.fromisoformat(hire_date_str)
        except ValueError:
            return HttpResponse("Invalid date format. Please use the ISO 8601 format (YYYY-MM-DD).")
        
         # Fetch the selected role and department
        role = Role.objects.get(id=role_id)
        dept = Department.objects.get(id=dept_id)
        new_emp = Employee(first_name=first_name, last_name=last_name, salary=salary, bonus=bonus, phone=phone, dept=dept, role=role, hire_date=hire_date)
        new_emp.save()
        
        return render(request, 'add_emp.html', {
            'success_message': 'Employee added successfully',
            'roles': Role.objects.all(),
            'departments': Department.objects.all()
        })


    elif request.method == 'GET':
        roles = Role.objects.all()
        departments = Department.objects.all()
        return render(request, 'add_emp.html', {
            'roles': roles,
            'departments': departments
        })
    else:
        return HttpResponse("An Exception Occured! Employee Has Not Been Added.")
    

def remove_emp(request):
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        employee = Employee.objects.get(id=employee_id)
        employee.delete()
        return render(request, 'remove_emp.html', {
            'success_message': 'Employee removed successfully',})
    else:
        emps = Employee.objects.all()
        context = {
            'emps': emps
        }
        return render(request, 'remove_emp.html', context)

def filter_emp(request):
    if request.method == 'POST':
        name = request.POST['name']
        dept = request.POST['dept']
        role = request.POST['role']
        emps = Employee.objects.all()
    
        if name:
            emps= emps.filter(Q(first_name__icontains = name) |Q(last_name__icontains = name))
        if dept:
            emps= emps.filter(dept__name__contains= dept)
        if role:
            emps= emps.filter(role__name__contains = role)
        
        context = {
            'emps': emps
        }

        return render(request,'all_emp.html',context)
    
    elif request.method == 'GET':
        return render(request, 'filter_emp.html')
    else:
        return HttpResponse('An Exception Occured')
