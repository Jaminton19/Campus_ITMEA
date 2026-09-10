from django.contrib import messages
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db.models import Q
from django.shortcuts import get_object_or_404,redirect,render
from django.utils import timezone
from .forms import *
from .models import *

ROLE_GROUP={'admin':'Administrador','teacher':'Docente','student':'Estudiante'}
def role_required(role):
    def dec(view):
        def wrapper(request,*args,**kwargs):
            if not request.user.is_authenticated: return redirect('login')
            if request.user.role!=role:
                messages.error(request,'No tienes permiso para acceder a esta sección.')
                return redirect('dashboard')
            return view(request,*args,**kwargs)
        wrapper.__name__=view.__name__; wrapper.__doc__=view.__doc__; return wrapper
    return dec

def home_view(request): return render(request,'users/home.html')

def register_view(request):
    form=UserRegisterForm(request.POST or None,request.FILES or None)
    if request.method=='POST' and form.is_valid():
        user=form.save(commit=False); user.role='student'; user.set_password(form.cleaned_data['password']); user.save()
        group,_=Group.objects.get_or_create(name=ROLE_GROUP[user.role]); user.groups.add(group)
        messages.success(request,'Usuario creado correctamente.'); login(request,user); return redirect('dashboard')
    return render(request,'users/register.html',{'form':form})

def login_view(request):
    form=UserLoginForm(request,data=request.POST or None)
    if request.method=='POST' and form.is_valid(): login(request,form.get_user()); return redirect('dashboard')
    return render(request,'users/login.html',{'form':form})

@login_required
def logout_view(request):
    if request.method=='POST': logout(request); return redirect('login')
    return render(request,'users/logout_confirm.html')

@login_required
def dashboard(request):
    if request.user.role=='admin': return redirect('admin_dashboard')
    if request.user.role=='teacher': return redirect('teacher_dashboard')
    if request.user.role=='student': return redirect('student_dashboard')
    logout(request); return redirect('login')

@role_required('admin')
def admin_dashboard_view(request):
    ctx={'users':User.objects.all().order_by('-date_joined'),'groups':Grupo.objects.select_related('teacher'),'courses':Curso.objects.select_related('teacher','grupo'),'students':User.objects.filter(role='student'),'teachers':User.objects.filter(role='teacher')}
    return render(request,'users/dashboard_admin.html',ctx)

@role_required('admin')
def admin_users_view(request): return render(request,'users/admin_users.html',{'users':User.objects.all().order_by('-date_joined')})

@role_required('admin')
def admin_create_user(request):
    form=AdminUserCreateForm(request.POST or None,request.FILES or None)
    if request.method=='POST' and form.is_valid():
        u=form.save(commit=False); u.role=form.cleaned_data['role']; u.set_password(form.cleaned_data['password']); u.save(); g,_=Group.objects.get_or_create(name=ROLE_GROUP[u.role]); u.groups.add(g); messages.success(request,'Usuario creado.'); return redirect('admin_users')
    return render(request,'users/form.html',{'form':form,'title':'Crear usuario'})

@role_required('admin')
def admin_courses_view(request):
    courses=Curso.objects.select_related('teacher','grupo').order_by('-created_at')
    return render(request,'users/admin_courses.html',{'cursos':courses,'grupos':Grupo.objects.all(),'teachers':User.objects.filter(role='teacher'),'students':User.objects.filter(role='student')})

@role_required('admin')
def admin_create_group(request):
    form=GrupoForm(request.POST or None)
    if request.method=='POST' and form.is_valid(): form.save(); messages.success(request,'Grupo creado.'); return redirect('admin_courses')
    return render(request,'users/form.html',{'form':form,'title':'Crear grupo'})

@role_required('admin')
def admin_create_course(request):
    form=CursoForm(request.POST or None)
    if request.method=='POST' and form.is_valid(): form.save(); messages.success(request,'Curso creado.'); return redirect('admin_courses')
    return render(request,'users/form.html',{'form':form,'title':'Crear curso'})

@role_required('admin')
def admin_enroll(request):
    form=EnrollmentForm(request.POST or None)
    if request.method=='POST' and form.is_valid():
        obj,created=Enrollment.objects.get_or_create(student=form.cleaned_data['student'],curso=form.cleaned_data['curso'])
        messages.success(request,'Estudiante matriculado.' if created else 'El estudiante ya estaba matriculado.'); return redirect('admin_courses')
    return render(request,'users/form.html',{'form':form,'title':'Matricular estudiante'})

@role_required('admin')
def admin_reports_view(request): return render(request,'users/admin_reports.html',{'courses':Curso.objects.all(),'enrollments':Enrollment.objects.select_related('student','curso')})

@role_required('teacher')
def teacher_dashboard_view(request):
    courses=Curso.objects.filter(teacher=request.user,active=True).select_related('grupo').prefetch_related('enrollments')
    return render(request,'users/dashboard_teacher.html',{'courses':courses})

@role_required('teacher')
def teacher_students_view(request):
    courses=Curso.objects.filter(teacher=request.user)
    students=User.objects.filter(enrollments__curso__teacher=request.user).distinct()
    return render(request,'users/teacher_students.html',{'courses':courses,'students':students})

@role_required('teacher')
def teacher_reports_view(request):
    courses=Curso.objects.filter(teacher=request.user); return render(request,'users/teacher_reports.html',{'courses':courses})

@role_required('teacher')
def teacher_course_view(request,curso_id):
    curso=get_object_or_404(Curso.objects.select_related('grupo'),id=curso_id,teacher=request.user)
    alumnos=User.objects.filter(enrollments__curso=curso).distinct()
    return render(request,'users/dashboard_teacher_course.html',{'curso':curso,'alumnos':alumnos,'materiales':curso.materiales.all(),'anuncios':curso.anuncios.all(),'tareas':curso.tareas.all(),'evaluaciones':curso.evaluaciones.all()})

def teacher_owned(request,curso_id): return get_object_or_404(Curso,id=curso_id,teacher=request.user)
@role_required('teacher')
def add_material(request,curso_id):
    curso=teacher_owned(request,curso_id); form=MaterialForm(request.POST or None,request.FILES or None)
    if request.method=='POST' and form.is_valid(): o=form.save(commit=False); o.curso=curso; o.save(); messages.success(request,'Material publicado.'); return redirect('teacher_course',curso.id)
    return render(request,'users/form.html',{'form':form,'title':'Agregar material','back_url':'teacher_course','back_id':curso.id})
@role_required('teacher')
def add_announcement(request,curso_id):
    curso=teacher_owned(request,curso_id); form=AnnouncementForm(request.POST or None)
    if request.method=='POST' and form.is_valid(): o=form.save(commit=False); o.curso=curso; o.save(); messages.success(request,'Anuncio publicado.'); return redirect('teacher_course',curso.id)
    return render(request,'users/form.html',{'form':form,'title':'Nuevo anuncio','back_url':'teacher_course','back_id':curso.id})
@role_required('teacher')
def add_assignment(request,curso_id):
    curso=teacher_owned(request,curso_id); form=AssignmentForm(request.POST or None)
    if request.method=='POST' and form.is_valid(): o=form.save(commit=False); o.curso=curso; o.save(); messages.success(request,'Tarea creada.'); return redirect('teacher_course',curso.id)
    return render(request,'users/form.html',{'form':form,'title':'Nueva tarea','back_url':'teacher_course','back_id':curso.id})
@role_required('teacher')
def add_evaluation(request,curso_id):
    curso=teacher_owned(request,curso_id); form=EvaluationForm(request.POST or None)
    if request.method=='POST' and form.is_valid(): o=form.save(commit=False); o.curso=curso; o.save(); messages.success(request,'Evaluación creada.'); return redirect('teacher_course',curso.id)
    return render(request,'users/form.html',{'form':form,'title':'Nueva evaluación','back_url':'teacher_course','back_id':curso.id})
@role_required('teacher')
def grade_evaluation(request,evaluation_id):
    ev=get_object_or_404(Evaluation, id=evaluation_id, curso__teacher=request.user); students=User.objects.filter(enrollments__curso=ev.curso)
    if request.method=='POST':
        for s in students:
            val=request.POST.get(f'grade_{s.id}')
            if val!='': EvaluationGrade.objects.update_or_create(evaluation=ev,student=s,defaults={'grade':val,'observation':request.POST.get(f'obs_{s.id}','')})
        messages.success(request,'Calificaciones guardadas.'); return redirect('teacher_course',ev.curso.id)
    grades={g.student_id:g for g in ev.grades.all()}; return render(request,'users/grade_evaluation.html',{'evaluation':ev,'students':students,'grades':grades})
@role_required('teacher')
def grade_assignments(request,curso_id):
    curso=teacher_owned(request,curso_id); tasks=curso.tareas.all()
    if request.method=='POST':
        for sub in Submission.objects.filter(assignment__curso=curso):
            val=request.POST.get(f'grade_{sub.id}')
            if val!='': sub.grade=val; sub.feedback=request.POST.get(f'feedback_{sub.id}',''); sub.save()
        messages.success(request,'Notas de tareas guardadas.')
    return render(request,'users/grade_assignments.html',{'curso':curso,'submissions':Submission.objects.filter(assignment__curso=curso).select_related('student','assignment')})
@role_required('teacher')
def attendance(request,curso_id):
    curso=teacher_owned(request,curso_id); students=User.objects.filter(enrollments__curso=curso); date=request.POST.get('date') or request.GET.get('date') or timezone.localdate().isoformat()
    if request.method=='POST':
        for s in students: Attendance.objects.update_or_create(curso=curso,student=s,date=date,defaults={'present':request.POST.get(f'present_{s.id}')=='on','observation':request.POST.get(f'obs_{s.id}','')})
        messages.success(request,'Asistencia guardada.'); return redirect('attendance',curso.id)
    records={a.student_id:a for a in Attendance.objects.filter(curso=curso,date=date)}
    return render(request,'users/attendance.html',{'curso':curso,'students':students,'records':records,'date':date})

@role_required('student')
def student_dashboard_view(request):
    courses=Curso.objects.filter(enrollments__student=request.user,active=True).select_related('teacher','grupo').distinct()
    return render(request,'users/dashboard_student.html',{'courses':courses})
@role_required('student')
def student_course_view(request,curso_id):
    curso=get_object_or_404(Curso.objects.filter(enrollments__student=request.user),id=curso_id)
    return render(request,'users/student_course.html',{'curso':curso,'materiales':curso.materiales.all(),'anuncios':curso.anuncios.all(),'tareas':curso.tareas.all(),'evaluaciones':curso.evaluaciones.all(),'submissions':{s.assignment_id:s for s in Submission.objects.filter(assignment__curso=curso,student=request.user)}})
@role_required('student')
def submit_assignment(request,assignment_id):
    task=get_object_or_404(Assignment, id=assignment_id,curso__enrollments__student=request.user); obj,created=Submission.objects.get_or_create(assignment=task,student=request.user); form=SubmissionForm(request.POST or None,request.FILES or None,instance=obj)
    if request.method=='POST' and form.is_valid(): form.save(); messages.success(request,'Entrega guardada.'); return redirect('student_course',task.curso.id)
    return render(request,'users/form.html',{'form':form,'title':f'Entregar: {task.title}'})
@role_required('student')
def student_profile_view(request): return render(request,'users/student_profile.html')
@role_required('student')
def student_reports_view(request): return render(request,'users/student_reports.html')
