from django import forms
from .models import Project, Task
from django.contrib.auth import get_user_model

User = get_user_model()

class ProjectForm(forms.ModelForm):

    assigned_manager = forms.ModelChoiceField(
        queryset=User.objects.filter(role='manager'),
        empty_label="Select Manager"
    )
    class Meta:
        model = Project
        fields = ['title', 'description', 'assigned_manager', 'start_date', 'end_date', 'status']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['assigned_manager'].queryset = User.objects.filter(role='manager')

class TaskForm(forms.ModelForm):
        assigned_to = forms.ModelChoiceField(
            queryset=User.objects.filter(role='user'),
            empty_label="Select User"
        )
        class Meta:
            model = Task
            fields = ['project', 'title', 'description', 'assigned_to', 'priority', 'due_date']
            widgets = {
                'due_date': forms.DateInput(attrs={'type': 'date'}),
            }
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['assigned_to'].queryset = User.objects.filter(role='user')
        # class Meta:
        #  model = Task
        #  fields = ['project', 'title', 'description', 'assigned_to', 'priority', 'due_date']
        #  widgets = {
        #     'due_date': forms.DateInput(attrs={'type': 'date'}),
        # }
        # def __init__(self, *args, **kwargs):
        #   super().__init__(*args, **kwargs)
        #   self.fields['assigned_to'].queryset = User.objects.filter(role='user')    

class UserTaskUpdateForm(forms.ModelForm):
        class Meta:
         model = Task
         fields = ['status', 'progress_note', 'issue_note', 'expected_completion_date']
         widgets = {
            'expected_completion_date': forms.DateInput(attrs={'type': 'date'}),
            'progress_note': forms.Textarea(attrs={'rows': 3}),
            'issue_note': forms.Textarea(attrs={'rows': 3}),
        }
class ProjectProgressUpdateForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_progress', 'project_notes']
        widgets = {
            'project_notes': forms.Textarea(attrs={'rows': 4}),
        }         