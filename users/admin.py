from django.contrib import admin
from .models import *
admin.site.register([User,Grupo,Curso,Enrollment,Material,Announcement,Assignment,Submission,Evaluation,EvaluationGrade,Attendance])
