from django.shortcuts import render, redirect
from .models import TableBooking
from django.http import HttpResponse
from django.contrib import messages
from datetime import datetime, date, time
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login  as auth_login
from .models import Employee, Role ,Department
from django.db.models import Q

# Create your views here.
def emp(request):
    return render(request,'emp.html')

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


def book_table(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        number = request.POST.get('number')
        person = request.POST.get('person')
        date = request.POST.get('date')

        # Validate the input data
        # if not name or not email or not number or not person or not booking_date:
        #     messages.error(request, "Please fill in all the required fields.")
        #     return redirect('book_table')

        # try:
        #     # Convert the booking_date string to a datetime object
        #     booking_date = datetime.strptime(booking_date, '%Y-%m-%d').date()
        # except ValueError:
        #     messages.error(request, "Invalid date format. Please enter the date in the format YYYY-MM-DD.")
        #     return redirect('book_table')

        # Check if the requested number of persons is available
        # available_slots = TableBooking.objects.filter(booking_date=booking_date).aggregate(Sum('persons'))['persons__sum']
        # if available_slots is None:
        #     available_slots = 0
        # remaining_slots = 10 - available_slots  # Assuming a maximum capacity of 10 persons
        # if int(person) > remaining_slots:
        #     messages.error(request, f"Sorry, there are only {remaining_slots} slots available on the requested date.")
        #     return redirect('book_table')
        if name !='' and email !='' and number !='' and date !='' and person != '':
            # Create a new TableBooking object and save it to the database
            booking = TableBooking(Name=name, Email=email, Number=number, Person=person, Date=date)
            booking.save()
            return redirect ('/')
        
        # # Send a successful booking email
        # subject = "Table Booking Confirmation"
        # message = f"Dear {name},\n\nThank you for booking a table at our restaurant. Your booking details are as follows:\n\nName: {name}\nEmail: {email}\nPhone Number: {number}\nNumber of Persons: {person}\nBooking Date: {booking_date}\n\nWe look forward to serving you on the booked date.\n\nBest regards,\nRestaurant Team"
        # from_email = "your_restaurant@example.com"
        # recipient_list = [email]
        # send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        # messages.success(request, "Table booked successfully! You will receive a confirmation email shortly.")
        # return redirect('/')
        
    return render(request, 'book_table.html')

def login(request):
    if request.method=='POST':
       username=request.POST['username']
       password=request.POST['password']
       user= authenticate(request,username=username,password=password)
       if user is not None:
            auth_login(request,user)
            return redirect ('emp')
       else:
            return HttpResponse("Username or Password is incorrect!!!")
       
    return render(request,'login.html')

def index(request):
    return render(request, 'index.html')

def menu(request):
    return render(request,'menu.html')

def order(request):
    return render(request,'order.html')

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request, 'contact.html')
def book(request):
    return render(request,'book.html')



# def menu(request):
#     items = MenuItem.objects.all()
#     return render(request, 'menu.html', {'items': items})

# def order(request):
#     if request.method == 'POST':
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('order_success')
#     else:
#         form = OrderForm()
#     return render(request, 'order.html', {'form': form})

# def book_table(request):
#     reservations = Reservation.objects.all()
#     return render(request, 'templates/book_table.html', {'reservations': reservations})

# def inventory(request):
#     items = InventoryItem.objects.all()
#     return render(request, 'templates/inventory.html', {'items': items})
