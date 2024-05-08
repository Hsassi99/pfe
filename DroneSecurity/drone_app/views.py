from django.conf import settings 
import os
from django.shortcuts import render, redirect 
from django import forms
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox
from django.shortcuts import render
import os
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
#torch bech n5admo yolo

from django.http import JsonResponse
from PIL import Image
import io
import torch
from django.http import StreamingHttpResponse
from django.apps import apps
import cv2


model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)


class CaptchaTestForm(forms.Form):
    captcha = ReCaptchaField()


def gen_frames():
    # Initialize video capture
    cap = cv2.VideoCapture(0)  # Change this to your camera ID or video source URL
    if not cap.isOpened():
        print("Error: Could not open video source.")
        return
    
    # Get the YOLO model loaded in apps.py
    app_config = apps.get_app_config('drone_app')
    model = app_config.model

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert frame to YOLOv5 compatible format and make predictions
        results = model(frame)
        
        # Render detections on the frame
        frame = results.render()[0]

        # Encode the frame in JPEG format
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue

        # Convert the buffer to bytes and yield
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    
    cap.release()

def video_feed(request):
    return StreamingHttpResponse(gen_frames(), content_type='multipart/x-mixed-replace; boundary=frame')



def home(request):
    print(os.path.join(settings.BASE_DIR, 'drone_app/templates'))
    return render(request, 'drone_app/home.html')

def setting(request):
    return render(request, 'drone_app/settings.html')
def stream(request):
    return render(request, 'drone_app/stream.html')
def admin_data(request):
    return render(request, 'drone_app/admin_data.html')
def problems_detected(request):
    return render(request, 'drone_app/problems.html')
def about_us(request):
    return render(request, 'drone_app/about_us.html')

def inscription(request):
    return render(request, 'drone_app/inscription.html')

def inscription_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user:
                login(request, user)
                messages.success(request, "Registration successful.")
                return redirect('home')  # Redirect to home or any other page
            else:
                messages.error(request, "Authentication failed. Please try again.")
        else:
            messages.error(request, "Invalid form submission. Please check the data provided.")
    else:
        form = UserCreationForm()
    return render(request, 'drone_app/inscription.html', {'form': form})


def img_view(request):

    img_directory = os.path.join('C:/Users/hsass/Desktop/drone1/DroneSecurity', 'static', 'img')
    img_files = [f for f in os.listdir(img_directory) if os.path.isfile(os.path.join(img_directory, f))]
    print("Image files:", img_files)

    context = {'images': img_files,}
    return render(request, 'drone_app/img.html', context)




def login_view(request):
    print("Method:", request.method)  # Print the method to debug
    context = {'form': CaptchaTestForm()}  # Always send a fresh form for GET requests

    if request.method == 'POST':
        form = CaptchaTestForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')

        if form.is_valid():
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('http://127.0.0.1:8000/drone_app/problems/')
            else:
                context['error_message'] = 'Invalid username or password'
        else:
            context['error_message'] = 'Invalid CAPTCHA'

    return render(request, 'drone_app/admin_data.html', context)





def problem_view(request):
    problem_file_path = os.path.join('C:/Users/hsass/Desktop/drone1/DroneSecurity', 'static', 'problem.txt')
    try:
        with open(problem_file_path, 'r') as file:
            problem_details = file.readlines()
        
        line_count = {}
        for line in problem_details:
            if line in line_count:
                line_count[line] += 1
            else:
                line_count[line] = 1
        
        problem_details = [line for line in problem_details if line_count[line] == 1]
    except FileNotFoundError:
        problem_details = ["Problem details not available."]

    context = {
        'problem_details': problem_details
    }
    print("View was called")
    return render(request, 'drone_app/problems.html', context)

