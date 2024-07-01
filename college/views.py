from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
import datetime
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Sum, Count
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
# Create your views here.
def index(request):
    return render(request, 'college/index.html')


def courses(request):
    return render(request, 'college/courses.html')

def staff(request):
    return render(request, 'college/teaching_staff.html')




def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']

        # Prepare the email message
        full_message = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
        
        # Send email
        send_mail(
            subject,
            full_message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.CONTACT_EMAIL],  # Ensure CONTACT_EMAIL is defined in your settings
        )

        # Success message
        messages.success(request, 'تم إرسال رسالتك بنجاح!')
        return redirect('contact')

    return render(request, 'college/contact_us.html')