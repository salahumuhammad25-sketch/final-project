from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from projects.models import Project, Task
from accounts.models import CustomUser

@login_required
def reports_dashboard(request):
    if request.user.role not in ['admin', 'manager']:
        return render(request, 'reports/permission_denied.html')

@login_required
def reports_dashboard(request):
    context = {
    
        'total_users': CustomUser.objects.filter(role='user').count(),

        # Managers count
        'total_managers': CustomUser.objects.filter(role='manager').count(),

        # All users except admin
        'total_non_admin': CustomUser.objects.exclude(role='admin').count(),

        'total_projects': Project.objects.count(),
        'total_tasks': Task.objects.count(),
        'completed_tasks': Task.objects.filter(status='completed').count(),
        'pending_tasks': Task.objects.filter(status='pending').count(),
        'in_progress_tasks': Task.objects.filter(status='in_progress').count(),
        'overdue_tasks': Task.objects.filter(status='overdue').count(),
        'user_role': request.user.role,
    }

    return render(request, 'reports/dashboard.html', context)