
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Project, Task
from .forms import ProjectForm, TaskForm, UserTaskUpdateForm
from .forms import ProjectProgressUpdateForm

def can_manage(user):
    return user.role in ['admin', 'manager']

@login_required
def project_update_progress(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if request.user.role != 'user':
        messages.error(request, 'Only users can update project progress.')
        return redirect('project_list')

    form = ProjectProgressUpdateForm(request.POST or None, instance=project)

    if request.method == 'POST':
        if form.is_valid():
            progress = form.save(commit=False)
            progress.updated_by_user = request.user
            progress.save()
            messages.success(request, 'Project progress updated successfully.')
            return redirect('project_list')

    return render(request, 'projects/project_update_progress.html', {
        'form': form,
        'project': project
    })

@login_required
def project_list(request):
    if request.user.role == 'admin':
        projects = Project.objects.all()
    elif request.user.role == 'manager':
        projects = Project.objects.filter(assigned_manager=request.user)
    else:
        projects = Project.objects.filter(tasks__assigned_to=request.user).distinct()

    return render(request, 'projects/project_list.html', {'projects': projects})

@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    # tasks = project.tasks.all()
    return render(request, 'projects/project_detail.html', {'project': project})
@login_required
def project_progress(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'projects/project_progress.html', {'project': project})

    
    return render(request, 'projects/project_progress.html', context)

@login_required
def project_create(request):
    if not can_manage(request.user):
        messages.error(request, 'Access denied.')
        return redirect('project_list')

    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = request.user
            project.save()
            messages.success(request, 'Project created successfully.')
            return redirect('project_list')
    else:
        form = ProjectForm()

    return render(request, 'projects/project_form.html', {'form': form, 'title': 'Create Project'})

@login_required
def project_update(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if not can_manage(request.user):
        messages.error(request, 'Access denied.')
        return redirect('project_list')

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project updated successfully.')
            return redirect('project_list')
    else:
        form = ProjectForm(instance=project)

    return render(request, 'projects/project_form.html', {'form': form, 'title': 'Update Project'})

@login_required
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if not can_manage(request.user):
        messages.error(request, 'Access denied.')
        return redirect('project_list')

    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Project deleted successfully.')
        return redirect('project_list')

    return render(request, 'projects/project_confirm_delete.html', {'project': project})

@login_required
def task_list(request):
    if request.user.role == 'admin':
        tasks = Task.objects.all()
    elif request.user.role == 'manager':
        tasks = Task.objects.filter(project__assigned_manager=request.user)
    else:
        tasks = Task.objects.filter(assigned_to=request.user)

    return render(request, 'projects/task_list.html', {'tasks': tasks})

@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'projects/task_detail.html', {'task': task})

@login_required
def task_create(request):
    if not can_manage(request.user):
        messages.error(request, 'Access denied.')
        return redirect('task_list')

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.status = 'pending'
            task.save()
            messages.success(request, 'Task created successfully.')
            return redirect('task_list')
    else:
        form = TaskForm()

    return render(request, 'projects/task_form.html', {'form': form, 'title': 'Create Task'})

@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.user.role not in ['admin', 'manager', 'user']:
        messages.error(request, 'Access denied.')
        return redirect('task_list')

    if request.user.role == 'user' and task.assigned_to != request.user:
        messages.error(request, 'Access denied.')
        return redirect('task_list')

    if request.method == 'POST':
        if request.user.role == 'user':
            form = UserTaskUpdateForm(request.POST, instance=task)
            if form.is_valid():
                form.save()
                messages.success(request, 'Task progress updated successfully.')
                return redirect('task_list')
        else:
            form = TaskForm(request.POST, instance=task)
            if form.is_valid():
                updated_task = form.save(commit=False)
                updated_task.assigned_by = task.assigned_by or request.user
                updated_task.save()
                messages.success(request, 'Task updated successfully.')
                return redirect('task_list')
    else:
        if request.user.role == 'user':
            form = UserTaskUpdateForm(instance=task)
        else:
            form = TaskForm(instance=task)

    return render(request, 'projects/task_form.html', {
        'form': form,
        'title': 'Update Task',
        'task': task
    })

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if not can_manage(request.user):
        messages.error(request, 'Access denied.')
        return redirect('task_list')

    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted successfully.')
        return redirect('task_list')

    return render(request, 'projects/task_confirm_delete.html', {'task': task})