from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from mess.models import Student
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash

# Create your views here.

def user_signup(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        # qr_code = request.POST.get('qr_code') # gotta create through our own methods here

        student = Student(name=name, qr_code=qr_code, password=password)
        # You might perform additional checks here before saving the student
        student.save()
        return HttpResponse("Student created successfully!") # render same page with message later
    return HttpResponse("Method not allowed.")

def user_login(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        try:
            student = Student.objects.get(name=name, password=password)
            return HttpResponse("Login successful!") # send to main page from here
        except:
            return HttpResponse("Invalid credentials. Please try again.") # render same page with message later
    return HttpResponse("Method not allowed.")

def change_password(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        try:
            student = Student.objects.get(name=name, password=old_password)
            student.password = new_password
            student.save()
            return HttpResponse("Password changed successfully!") # render same page with message
        except:
            return HttpResponse("Invalid.") # render same page with message
    return HttpResponse("Method not allowed.")

def hello(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render())
#########################################################################
#                        HELPER FUNCTIONS                               #
#########################################################################
def check_meal_consumption(meal_type, student_name, date):
    meal_types = {'BREAKFAST': 1, 'LUNCH': 2, 'DINNER': 4} 
    meal_flag = meal_types.get(meal_type.upper())  
    try:
        student = Student.objects.get(name=student_name)
    except Student.DoesNotExist:
        return False
    # Get the student's meal_data string and check if the meal was consumed on the given date
    meal_data = student.meal_data
    meal_at_date = int(meal_data[date])
    if meal_at_date & meal_flag: # bitwise AND with the flag
        return True
    else:
        return False