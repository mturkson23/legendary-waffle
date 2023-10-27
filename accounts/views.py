from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        # Create a form instance from POST data.
        form = UserCreationForm(request.POST)
        # Check if the form is valid.
        if form.is_valid():
            # Save the user to the database.
            form.save()
            # Redirect to the login page.
            return redirect('login')
    form = UserCreationForm()
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
    form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required(login_url='login')
def dashboard(request):
    return render(request, 'accounts/dashboard.html')
