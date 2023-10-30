from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import UserRegisterForm, UserLoginForm

# Create your views here.
def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        # Create a form instance from POST data.
        form = UserRegisterForm(request.POST)
        # Check if the form is valid.
        if form.is_valid():
            # Save the user to the database.
            form.save()
            # Redirect to the login page.
            return redirect('dashboard')
    form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        # Get the username and password from the request.
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate the user.
        user = authenticate(request, username=username, password=password)
        # If the user exists.
        if user is not None:
            # Log the user in.
            login(request, user)
            # Redirect to the home page.
            return redirect('dashboard')
    form = UserLoginForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required(login_url='login')
def dashboard(request):
    user_tickets = request.user.ticket_set.all()
    user_events = request.user.event_set.all()
    return render(request, 'accounts/dashboard.html', {'user_tickets': user_tickets, 'user_events': user_events})

@login_required(login_url='login')
def logout_user(request):
    logout(request)
    return redirect('index')
