import openai
import csv
from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from myapp.forms import CallBackForm
from django.http import HttpResponse
from django.utils import timezone
from django.views.generic import TemplateView
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
import cv2
import numpy as np
from insightface.app import FaceAnalysis
from telegram import Bot


# Create your views here.
def index(request):
    return render(request,'index.html')

# def about_us(request):
#     return render(request,'about_us.html')

# Replace 'YOUR_OPENAI_API_KEY' with your actual OpenAI API key
openai.api_key = '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'

def Ai(request, email):
    email_approval = get_object_or_404(EmailApproval, email=email)

    if request.method == 'POST':
        text = request.POST.get('user_input')
        print("User input:", text)

        # Perform OpenAI chat completion
        output = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"{text} in 50 words"}],
        )
        response = output['choices'][0]['message']['content']
        print("Response:", response)

        # Save user input and bot response to the database with associated email
        ChatMessage.objects.create(role="user", content=text, email=email_approval)
        ChatMessage.objects.create(role="bot", content=response, email=email_approval)

    # Retrieve chat messages associated with the email
    messages = ChatMessage.objects.filter(email=email_approval)

    return render(request, 'Ai_Teacher.html', {'messages': messages})

def clear_chat_history(request):
    ChatMessage.objects.all().delete()
    return redirect('ai', email='example@email.com')  # Change the email to the desired email




def email_approval(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')

        if email:
            email_approval, created = EmailApproval.objects.get_or_create(email=email)

            # Check if the admin has approved the email (you can implement your own logic here)
            if email_approval.approved:
                
                

                return redirect('ai', email=email)  # Redirect to the AI view with the email
            else:
                return render(request, 'email_approval.html', {'message': 'Email is pending approval'})

    return render(request, 'email_approval.html')


def admin_approval(request):
    if request.method == 'GET':
        pending_emails = EmailApproval.objects.filter(approved=False)
        return render(request, 'admin_approval.html', {'pending_emails': pending_emails})
    elif request.method == 'POST':
        email_id = request.POST.get('email_id')
        if email_id:
            email_approval = EmailApproval.objects.get(id=email_id)
            email_approval.approved = True
            email_approval.save()
        return redirect('admin_approval')



def request_callback(request):
    if request.method == 'POST':
        form = CallBackForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = CallBackForm()

    return render(request, 'contact.html', {'form': form})



# def download_csv(request):
#     if request.method == 'POST':
#         # Create the HttpResponse object with appropriate headers.
#         response = HttpResponse(content_type='text/csv')
#         response['Content-Disposition'] = f'attachment; filename="callbacks_{timezone.now().strftime("%Y-%m-%d")}.csv"'

#         writer = csv.writer(response)
#         # Write the header
#         writer.writerow(['Name', 'Email', 'Message', 'Created At'])

#         # Filter the records based on whether they have been exported
#         callbacks = CallBackRequest.objects.filter(exported=False)

#         for callback in callbacks:
#             writer.writerow([callback.name, callback.email, callback.message, callback.created_at])

#             # Mark the record as exported
#             callback.exported = True
#             callback.save(update_fields=['exported'])

#         return response
#     else:
#         # If the request is not a POST request, you can render a login page or any other page as needed.
#         return render(request, 'login.html')


def download_csv(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            # Authenticate the user
            user = form.get_user()
            login(request, user)
            # Create the HttpResponse object with appropriate headers.
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="callbacks_{timezone.now().strftime("%Y-%m-%d")}.csv"'

            writer = csv.writer(response)
            # Write the header
            writer.writerow(['Name', 'Email', 'Message', 'Contact No', 'Created At'])

            # Filter the records based on whether they have been exported
            callbacks = CallBackRequest.objects.filter(exported=False)

            for callback in callbacks:
                writer.writerow([callback.name, callback.email, callback.message, callback.mobile_no, callback.created_at])

                # Mark the record as exported
                callback.exported = True
                callback.save(update_fields=['exported'])

            return response
        
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


def trial(request):
    return render(request, 'trial.html')

def team_view(request):
    teams = Team.objects.all()
    return render(request, 'team.html', {'teams': teams})

# def add_member(request):
#     if request.method == "POST":
#         # Get the data from the request
#         image = request.FILES.get('image')
#         name = request.POST.get('name')
#         description = request.POST.get('description')

#         if image and name and description:
#             # Create a new Member instance and save it to the database
#             member = Members(image=image, name=name, description=description)
#             member.save()

#             return redirect('add-member')  # Redirect to a view that lists all members
#         else:
#             return HttpResponse("All fields are required")

#     return render(request, 'add-member.html')

class Tryus(TemplateView):
    template_name = "tryus.html"




# Initialize the FaceAnalysis object once during application startup
app_sc = FaceAnalysis(name='buffalo_sc', root='insightface_model', providers=['CPUExecutionProvider'])
app_sc.prepare(ctx_id=0, det_size=(640, 640), det_thresh=0.5)

def similarity_score_view(request):
    if request.method == 'POST' and request.FILES.get('image1') and request.FILES.get('image2'):
        image1 = request.FILES['image1']
        image2 = request.FILES['image2']

        # Process the uploaded images
        embedding1, error_message1 = get_embeddings(image1)
        embedding2, error_message2 = get_embeddings(image2)

        if embedding1 is not None and embedding2 is not None:
            # Calculate the similarity score
            similarity = calculate_similarity(embedding1, embedding2)
            if similarity is not None:
                return render(request, 'similarity.html', {'similarity': similarity})
            else:
                error_message = "Error calculating similarity."
                return render(request, 'similarity.html', {'error_message': error_message})
        else:
            error_message = error_message1 or error_message2  # Choose the first non-empty error message
            return render(request, 'similarity.html', {'error_message': error_message})

    return render(request, 'similarity.html')


def get_embeddings(image):
    try:
        img_arr = cv2.imdecode(np.fromstring(image.read(), np.uint8), cv2.IMREAD_COLOR)
        result = app_sc.get(img_arr)

        if result is not None:
            if len(result) > 1:
                error_message = "Multiple faces detected "
                return None, error_message  # Return both None and error message for multiple faces detected
            if len(result) == 0:
                error_message = "No faces detected "
                return None, error_message  # Return both None and error message for no faces detected
            embedding = result[0].embedding
            return embedding, None  # Return the embedding and no error message

    except Exception as e:
        error_message = "Error processing the images."
        print(f"Error: {e}")
        return None, error_message  # Return None and error message for general processing errors



def calculate_similarity(embedding1, embedding2):
    if embedding1 is None or embedding2 is None:
        return None  # Handle cases where face(s) are not detected

    similarity_score = np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))
    return round(similarity_score * 100, 2)
