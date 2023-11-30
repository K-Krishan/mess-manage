from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from mess.models import Student
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from .qr import encode, decode
from django.conf import settings
from PIL import Image

# Create your views here.

def signup_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        # edit qr code and save
        qr_code=name
        password = request.POST.get('password')
        # guard for student existing
        try:
            student = Student.objects.get(name=student_name)
            return HttpResponse("Student already exists")
        except:
            pass
        student = Student(name=name, qr_code=qr_code, password=password, meal_data="0000000000000000000000000000000")
        # You might perform additional checks here before saving the student
        student.save()
        imagedata = encode(qr_code)
        qr_code_image = imagedata.png(f'{settings.QR_CODE_DIR}/{name}.png', scale=6)

        # return HttpResponse("Student created successfully!") # send to profile
        return render(request, 'profile.html', {'user_name': name, 'image_path': f'{name}.png', 'meal_data': student.meal_data})
    return render(request, 'signup.html')

def login_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')

        try:
            student = Student.objects.get(name=name, password=password)
            # Perform additional verification if needed
            # return HttpResponse("Login successful!") # send to profile
            return render(request, 'profile.html', {'user_name': name, 'image_path': f'{name}.png', 'meal_data': student.meal_data})

        except Student.DoesNotExist:
            return HttpResponse("Invalid credentials. Please try again.")

    return render(request, 'login.html')

def QRlogin_view(request):
    if request.method == 'POST':
        qr_image = request.FILES.get('qr_image')

        if qr_image:
            print(qr_image)
            qr_text = decode(qr_image)
            print(qr_text)
            if qr_text:
                try:
                    student = Student.objects.get(qr_code=qr_text)
                    # return HttpResponse(f"Login successful! Welcome, {student.name}!") # send to profile
                    return render(request, 'profile.html', {'user_name': student.name, 'image_path': f'{student.name}.png', 'meal_data': student.meal_data})
                except Student.DoesNotExist:
                    return HttpResponse("User not found. Please try again.")
            else:
                return HttpResponse("Invalid QR code. Please try again.")
        else:
            return HttpResponse("No QR code submitted. Please select an image.")

    return render(request, 'loginqr.html')

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