from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

class CampusUserManager(UserManager):
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields['role'] = 'admin'
        return super().create_superuser(username, email, password, **extra_fields)


class User(AbstractUser):
    ROLE_CHOICES=(('admin','Administrador'),('teacher','Docente'),('student','Estudiante'))
    role=models.CharField(max_length=20,choices=ROLE_CHOICES,default='student')
    objects = CampusUserManager()
    phone=models.CharField(max_length=20,blank=True,null=True)
    document=models.CharField(max_length=30,blank=True,null=True)
    profile_image=models.ImageField(upload_to='profiles/',blank=True,null=True)
    full_name=models.CharField(max_length=150,blank=True,null=True)
    birth_date=models.DateField(blank=True,null=True)
    start_date=models.DateField(blank=True,null=True)
    def __str__(self): return self.full_name or self.username

class Grupo(models.Model):
    name=models.CharField(max_length=100)
    program=models.CharField(max_length=100)
    teacher=models.ForeignKey(User,on_delete=models.CASCADE,limit_choices_to={'role':'teacher'},related_name='grupos_docente')
    active=models.BooleanField(default=True)
    def __str__(self): return f'{self.program} - {self.name}'

class Curso(models.Model):
    name=models.CharField(max_length=150)
    description=models.TextField(blank=True,null=True)
    grupo=models.ForeignKey(Grupo,on_delete=models.CASCADE,related_name='cursos')
    teacher=models.ForeignKey(User,on_delete=models.CASCADE,limit_choices_to={'role':'teacher'},related_name='cursos_docente')
    created_at=models.DateTimeField(auto_now_add=True)
    active=models.BooleanField(default=True)
    def __str__(self): return self.name

class Enrollment(models.Model):
    student=models.ForeignKey(User,on_delete=models.CASCADE,limit_choices_to={'role':'student'},related_name='enrollments')
    curso=models.ForeignKey(Curso,on_delete=models.CASCADE,related_name='enrollments')
    grade=models.DecimalField(max_digits=5,decimal_places=2,blank=True,null=True)
    description=models.TextField(blank=True,null=True)
    percentage=models.DecimalField(max_digits=5,decimal_places=2,blank=True,null=True)
    observations=models.TextField(blank=True,null=True)
    enrolled_at=models.DateTimeField(auto_now_add=True)
    class Meta: constraints=[models.UniqueConstraint(fields=['student','curso'],name='unique_student_curso')]
    def __str__(self): return f'{self.student} - {self.curso}'

class Material(models.Model):
    curso=models.ForeignKey(Curso,on_delete=models.CASCADE,related_name='materiales')
    title=models.CharField(max_length=200)
    description=models.TextField(blank=True)
    file=models.FileField(upload_to='materials/',blank=True,null=True)
    url=models.URLField(blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.title

class Announcement(models.Model):
    curso=models.ForeignKey(Curso,on_delete=models.CASCADE,related_name='anuncios')
    title=models.CharField(max_length=200)
    body=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.title

class Assignment(models.Model):
    curso=models.ForeignKey(Curso,on_delete=models.CASCADE,related_name='tareas')
    title=models.CharField(max_length=200)
    description=models.TextField()
    due_date=models.DateTimeField(blank=True,null=True)
    points=models.DecimalField(max_digits=6,decimal_places=2,default=100)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.title

class Submission(models.Model):
    assignment=models.ForeignKey(Assignment,on_delete=models.CASCADE,related_name='submissions')
    student=models.ForeignKey(User,on_delete=models.CASCADE,related_name='submissions')
    text=models.TextField(blank=True)
    file=models.FileField(upload_to='submissions/',blank=True,null=True)
    submitted_at=models.DateTimeField(auto_now=True)
    grade=models.DecimalField(max_digits=6,decimal_places=2,blank=True,null=True)
    feedback=models.TextField(blank=True)
    class Meta: constraints=[models.UniqueConstraint(fields=['assignment','student'],name='unique_assignment_student')]

class Evaluation(models.Model):
    curso=models.ForeignKey(Curso,on_delete=models.CASCADE,related_name='evaluaciones')
    title=models.CharField(max_length=200)
    weight=models.DecimalField(max_digits=5,decimal_places=2,default=100)
    date=models.DateField(blank=True,null=True)
    def __str__(self): return self.title

class EvaluationGrade(models.Model):
    evaluation=models.ForeignKey(Evaluation,on_delete=models.CASCADE,related_name='grades')
    student=models.ForeignKey(User,on_delete=models.CASCADE,related_name='evaluation_grades')
    grade=models.DecimalField(max_digits=5,decimal_places=2,blank=True,null=True)
    observation=models.TextField(blank=True)
    class Meta: constraints=[models.UniqueConstraint(fields=['evaluation','student'],name='unique_evaluation_student')]

class Attendance(models.Model):
    curso=models.ForeignKey(Curso,on_delete=models.CASCADE,related_name='attendances')
    student=models.ForeignKey(User,on_delete=models.CASCADE,related_name='attendances')
    date=models.DateField()
    present=models.BooleanField(default=True)
    observation=models.CharField(max_length=255,blank=True)
    class Meta: constraints=[models.UniqueConstraint(fields=['curso','student','date'],name='unique_attendance')]
