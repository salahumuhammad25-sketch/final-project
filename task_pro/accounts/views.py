from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignupForm, ProfileForm
from .models import CustomUser
from projects.models import Project, Task

def home(request):
    return render(request, 'home.html')

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully. Please login.')
            return redirect('login')
    else:
        form = SignupForm()

    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if user.is_superuser:
                return redirect('/admin/')
            else:
                return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    user = request.user

    if user.role == 'admin':
        context = {
            'total_users': CustomUser.objects.filter(
                is_superuser=False, 
                is_staff=False,
                is_active=True
                ).count(),
            
            'total_projects': Project.objects.count(),
            'total_tasks': Task.objects.count(),
            'completed_tasks': Task.objects.filter(status='completed').count(),
            'pending_tasks': Task.objects.filter(status='pending').count(),
            'my_projects': Project.objects.all()[:5],
            'my_tasks': Task.objects.all()[:5],
        }
    elif user.role == 'manager':
        manager_projects = Project.objects.filter(assigned_manager=user)
        manager_tasks = Task.objects.filter(project__assigned_manager=user)
        context = {
            'total_users': CustomUser.objects.filter(
                role='user' ,
                is_staff=False,
                is_superuser=False,
                is_active=True
                ).count(),
            'total_projects': manager_projects.count(),
            'total_tasks': manager_tasks.count(),
            'completed_tasks': manager_tasks.filter(status='completed').count(),
            'pending_tasks': manager_tasks.filter(status='pending').count(),
            'my_projects': manager_projects[:5],
            'my_tasks': manager_tasks[:5],
        }
    else:
        user_tasks = Task.objects.filter(assigned_to=user)
        context = {
            'total_users': None,
            'total_projects': Project.objects.filter(tasks__assigned_to=user).distinct().count(),
            'total_tasks': user_tasks.count(),
            'completed_tasks': user_tasks.filter(status='completed').count(),
            'pending_tasks': user_tasks.filter(status='pending').count(),
            'my_projects': Project.objects.filter(tasks__assigned_to=user).distinct()[:5],
            'my_tasks': user_tasks[:5],
        }

    return render(request, 'accounts/dashboard.html', context)

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)

    return render(request, 'accounts/profile.html', {'form': form})

@login_required
def user_list(request):
    if request.user.role != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')

    users = User.objects.filter(is_active=True, is_superuser=False)
    return render(request, 'accounts/user_list.html', {'users': users})