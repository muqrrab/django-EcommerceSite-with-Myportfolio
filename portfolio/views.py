import json
from unicodedata import name
from django.http import JsonResponse
from django.shortcuts import redirect, render
import mimetypes
# import os module
import os
# Import HttpResponse module
from django.http.response import HttpResponse
# Import render module
from django.shortcuts import render
from .models import Contact

# Create your views here.

def index(request):
    params = {}
    return render(request, 'portfolio/index.html',params)

def df(request, filename='Resume.pdf'):
    if filename != '':
        # Define Django project base directory
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # Define the full file path
        filepath = BASE_DIR + '/files/' + filename
        # Open the file for reading content
        path = open(filepath, 'rb')
        # Set the mime type
        mime_type, _ = mimetypes.guess_type(filepath)
        # Set the return value of the HttpResponse
        response = HttpResponse(path, content_type=mime_type)
        # Set the HTTP header for sending to browser
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        # Return the response value
        return response
    else:
        # Load the template
        return render(request, 'Resume.pdf')

def contact(request):
    return redirect(index)

def formsubmission(request):
    # if request.method == 'POST':
    #     name = request.POST.get('InputName')
    #     email = request.POST.get('InputEmail')
    #     subject = request.POST.get('InputSubject')
    #     msg = request.POST.get('InputMessage')
    #     print(name)

    data = json.loads(request.body)
    name = data['name']
    email = data['email']
    subject = data['subject']
    msg = data['message']

    contact = Contact.objects.create(
        name=name,
        email=email,
        subject = subject,
        message= msg
    )
    return JsonResponse('Payment Complete', safe=False)