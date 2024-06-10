from django.conf import settings 
import os
from django import forms
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
import requests

from django.db import connection
from django.http import HttpResponse

import socket
from django.http import HttpResponseRedirect
from django.urls import reverse

#torch bech n5admo yolo

from django.http import JsonResponse
from PIL import Image
import io
import torch
from django.http import StreamingHttpResponse
from django.apps import apps
import cv2
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
import face_recognition


def load_face_encodings(folder_path):
    """Loads all face encodings from images in the given folder."""
    face_encodings = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.jpg') or filename.endswith('.png'):  # Check for image files
            image_path = os.path.join(folder_path, filename)
            image = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(image)
            if encodings:
                face_encodings.append(encodings[0])  # Assume one face per image
    return face_encodings


def compare_faces(folder1, folder2):
    """Compares faces from two folders and prints the number of matches."""
    faces_folder1 = load_face_encodings(folder1)
    faces_folder2 = load_face_encodings(folder2)
    matches_count = 0

    for face1 in faces_folder1:
        for face2 in faces_folder2:
            result = face_recognition.compare_faces([face1], face2)
            if result[0]:  # If faces match
                matches_count += 1

    print(f"Number of matching faces: {matches_count}")
    return matches_count


know = compare_faces('C:/Users/hsass/Desktop/drone1/DroneSecurity/static/person', 'C:/Users/hsass/Desktop/drone1/DroneSecurity/static/img')
file_path_pro = 'C:/Users/hsass/Desktop/drone1/DroneSecurity/static/problem.txt'
def update_problem_file(know, file_path):
    if know == 0:
        # Attempt to read the existing content of the file
        try:
            with open(file_path, 'r') as file:
                contents = file.read()
                # Check if 'unknown person' is already in the file
                if 'unknown person' not in contents.lower():
                    # 'unknown person' not found, proceed to write it to the file
                    with open(file_path, 'a') as file:
                        file.write('unknown person\n')
                    print("Written 'unknown person' to the file.")
                else:
                    print("No update needed, 'unknown person' is already in the file.")
        except FileNotFoundError:
            # File does not exist, create the file and write the entry
            with open(file_path, 'w') as file:
                file.write('unknown person\n')
            print("File not found, created the file and wrote 'unknown person'.")
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print("Condition 'know == 0' not met, no updates made.")



model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

class CaptchaTestForm(forms.Form):
    captcha = ReCaptchaField()



def proxy_stream(request):
    stream_url = "http://192.168.110.168:5000/?video_feed"  # MJPEG Stream URL
    try:
        resp = requests.get(stream_url, stream=True)
        return StreamingHttpResponse(streaming_content=resp.iter_content(chunk_size=1024*1024),
                                     content_type=resp.headers['Content-Type'])
    except Exception as e:
        # Log the error for debugging
        print("Error connecting to the video stream: ", str(e))
        return StreamingHttpResponse("Error connecting to the video stream", status=500)



def gen_frames():
    # Initialize video capture
    cap = cv2.VideoCapture("http://192.168.110.168:5000/?video_feed")  # Your stream URL
    if not cap.isOpened():
        print("Error: Could not open video source.")
        return
    
    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # or use 'XVID'
    out = cv2.VideoWriter('static/videos/output.mp4', fourcc, 20.0, (640, 480))
    
    app_config = apps.get_app_config('drone_app')
    model = app_config.model
    
    # Initialize the last saved time
    last_saved_time = datetime.now() - timedelta(days=1)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Convert frame to YOLOv5 compatible format and make predictions
        results = model(frame)

        # Check for specific classes detected
        labels = results.xyxyn[0][:, -1].numpy()  # Assuming YOLOv5 returns labels as the last column
        person_detected = 0 in labels
        dog_detected = 16 in labels 
        cat_detected = 17 in labels
        # Get the current time
        current_time = datetime.now()

        # Save frame if specific objects are detected and at least 5 seconds have passed
        if (current_time - last_saved_time) >= timedelta(seconds=10) and (person_detected or dog_detected or cat_detected):
            timestamp = current_time.strftime("%Y%m%d_%H%M%S")
            cv2.imwrite(f'static/img/{timestamp}_detected.jpg', frame)
            last_saved_time = current_time  # Update last saved time
        
        # Render detections on the frame
        frame = results.render()[0]
        
        # Write the frame into the file 'output.mp4'
        out.write(frame)
        
        # Encode the frame in JPEG format
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue
        
        # Convert the buffer to bytes and yield
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    
    # Release everything if job is finished
    cap.release()
    out.release()

def video_feed(request):
    return StreamingHttpResponse(gen_frames(), content_type='multipart/x-mixed-replace; boundary=frame')



def send_command(request, command):
    url = 'https://pi/control'
    data = {'command': command}
    requests.post(url, data=data)
    messages.success(request, "Command sent successfully!")

    return redirect('setting')

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



# def list_users(request):
#     print("View called")  # Debug statement
#     with connection.cursor() as cursor:
#         cursor.execute("SELECT id, username, email, last_login FROM auth_user")
#         rows = cursor.fetchall()
#         print(rows)  # Debug output
def list_users(request):
    users = User.objects.all().values('id', 'username', 'email', 'last_login')
    print(users)  # Print the query results to the console to inspect them
    if not users:
        print("No users found in the database.")
    return render(request, 'drone_app/settings.html', {'users': list(users)})

    if not rows:
        print("No data found")  # Debug output
        return HttpResponse("No data found in the database.")

    users = [{'id': row[0], 'username': row[1], 'email': row[2], 'last_login': row[3]} for row in rows]
    print(users)  # Debug output

    return render(request, 'drone_app/settings.html', users)



def img_view(request):

    img_directory = os.path.join(settings.BASE_DIR, 'static', 'img')
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

            if user is not None and username=='Admin@123' and password=='Azerty@123':
                login(request, user)
                return redirect('setting')
            if user is not None:
                login(request, user)
                return redirect('problems_detected')  # Use the correct named URL pattern here
            else:
                context['error_message'] = 'Invalid username or password'
        else:
            context['error_message'] = 'Invalid CAPTCHA'

    return render(request, 'drone_app/admin_data.html', context)


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
            for field, error_list in form.errors.items():
                for error in error_list:
                    messages.error(request, f"{field}: {error}")
    else:
        form = UserCreationForm()
    return render(request, 'drone_app/inscription.html', {'form': form})




from django.shortcuts import render
from django.conf import settings
import os

def problems_detected(request):
    update_problem_file(know, file_path_pro)

    problem_file_path = 'C:/Users/hsass/Desktop/drone1/DroneSecurity/static/problem.txt'
    # problem_file_path = os.path.join(settings.BASE_DIR, 'static', 'problem.txt')
    # Dictionary mapping specific problems to recommended actions
    problem_actions = {
        'unknown person': 'Notify security.',
        'Dog or Cat': 'Check animal control policies.'
    }

    try:
        with open(problem_file_path, 'r') as file:
            problem_details = [line.strip() for line in file if line.strip()]

        line_count = {}
        for line in problem_details:
            if line in line_count:
                line_count[line] += 1
            else:
                line_count[line] = 1

        # Remove duplicates
        problem_details = [line for line in problem_details if line_count[line] == 1]

        # Determine actions needed for each problem
        actions_needed = [problem_actions.get(detail, 'No action needed.') for detail in problem_details]
        
    except FileNotFoundError:
        problem_details = ["Problem details not available."]
        actions_needed = ['No action available due to missing file.']

    context = {
        'problem_details': problem_details,
        'actions_needed': actions_needed
    }

    return render(request, 'drone_app/problems.html', context)




#user manager 


def delete_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            user = User.objects.get(username=username)
            user.delete()
            return HttpResponse("User deleted successfully.")
        except User.DoesNotExist:
            return HttpResponse("User does not exist.")

def change_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        new_password = request.POST.get('new_password')
        try:
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()
            return HttpResponse("Password changed successfully.")
        except User.DoesNotExist:
            return HttpResponse("User does not exist.")
        
def send_drone_command(request):
    if request.method == 'POST':
        command = request.POST.get('command')
        if command == 'block_stream':
            # Code to send command to block the stream
            pass
        elif command == 'shutdown':
            # Code to send command to shutdown the drone
            pass
        elif command == 'restart_stream':
            # Code to restart the stream
            pass
        return HttpResponse(f"Command '{command}' sent successfully.")
    return HttpResponse("Invalid request", status=400)

def trigger_backup(request):
    if request.method == 'POST':
        try:
        # Set up the socket connection to the backup VM
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(('20.199.91.247', 12345))  # Replace 'backup-vm-ip' and 'port'
            s.sendall(b'send')
            s.close()
            return HttpResponse("Backup database send to hamza1010sassi@gmail.com ,Check you email.")
        except Exception as e:
            return HttpResponse(f"Failed to initiate backup: {e}")