from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User,Grupo,Curso,Enrollment,Material,Announcement,Assignment,Evaluation,Submission

class UserRegisterForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput)
    confirm_password=forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model=User; fields=['username','email','phone','document','profile_image','full_name','birth_date','start_date']
        widgets={'birth_date':forms.DateInput(attrs={'type':'date'}),'start_date':forms.DateInput(attrs={'type':'date'})}
    def clean(self):
        d=super().clean()
        if d.get('password')!=d.get('confirm_password'): raise forms.ValidationError('Las contraseñas no coinciden.')
        return d

class AdminUserCreateForm(UserRegisterForm):
    role=forms.ChoiceField(choices=User.ROLE_CHOICES, label='Rol')


class UserLoginForm(AuthenticationForm):
    username=forms.CharField(label='Usuario'); password=forms.CharField(widget=forms.PasswordInput,label='Contraseña')

class GrupoForm(forms.ModelForm):
    class Meta: model=Grupo; fields=['program','name','teacher']
    def __init__(self,*a,**kw):
        super().__init__(*a,**kw); self.fields['teacher'].queryset=User.objects.filter(role='teacher',is_active=True)

class CursoForm(forms.ModelForm):
    class Meta: model=Curso; fields=['name','description','grupo','teacher','active']
    def __init__(self,*a,**kw):
        super().__init__(*a,**kw); self.fields['teacher'].queryset=User.objects.filter(role='teacher',is_active=True)

class EnrollmentForm(forms.ModelForm):
    class Meta: model=Enrollment; fields=['student','curso']
    def __init__(self,*a,**kw):
        super().__init__(*a,**kw); self.fields['student'].queryset=User.objects.filter(role='student',is_active=True)

class MaterialForm(forms.ModelForm):
    class Meta: model=Material; fields=['title','description','file','url']
class AnnouncementForm(forms.ModelForm):
    class Meta: model=Announcement; fields=['title','body']
class AssignmentForm(forms.ModelForm):
    class Meta:
        model=Assignment; fields=['title','description','due_date','points']; widgets={'due_date':forms.DateTimeInput(attrs={'type':'datetime-local'})}
class EvaluationForm(forms.ModelForm):
    class Meta:
        model=Evaluation; fields=['title','weight','date']; widgets={'date':forms.DateInput(attrs={'type':'date'})}
class SubmissionForm(forms.ModelForm):
    class Meta: model=Submission; fields=['text','file']
