from django.shortcuts import render, redirect
from django.contrib import messages

from application1.forms import LoginForm
from application1.models import login as LoginModel

def index (request):
    return render(request, 'index.html')
def category (request):
    return render(request, 'category.html')
def dashboard (request):
    return render(request, 'dashboard.html')
def entry1 (request):
    return render(request, 'entry1.html')
def manage (request):
    return render(request, 'manage.html')
def reports (request):
    return render(request, 'reports.html')
def settings (request):
    return render(request, 'settings.html')
def vehicle_entry (request):
    return render(request, 'vehicle_entry.html')
def vehicle_number (request):
    return render(request, 'vehicle_number.html')

def user_login(request):
    form=LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = LoginModel.objects.filter(
                username=username,
                password=password
            ).first()

            if user:
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid Username or Password")

    return render(request, 'index.html', {'form': form})
    