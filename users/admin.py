from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import (
    User,
    Grupo,
    Curso,
    Enrollment,
    Material,
    Announcement,
    Assignment,
    Submission,
    Evaluation,
    EvaluationGrade,
    Attendance,
)


class CampusUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'role',
            'phone',
            'document',
            'profile_image',
            'full_name',
            'birth_date',
            'start_date',
        )


class CampusUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'


@admin.register(User)
class CampusUserAdmin(UserAdmin):
    form = CampusUserChangeForm
    add_form = CampusUserCreationForm

    list_display = (
        'username',
        'full_name',
        'email',
        'role',
        'is_active',
    )

    list_filter = (
        'role',
        'is_active',
        'is_staff',
    )

    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Información personal', {
            'fields': (
                'full_name',
                'email',
                'phone',
                'document',
                'profile_image',
                'birth_date',
                'start_date',
            )
        }),
        ('Rol', {
            'fields': ('role',)
        }),
        ('Permisos', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            )
        }),
        ('Fechas', {
            'fields': (
                'last_login',
                'date_joined',
            )
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'password1',
                'password2',
                'email',
                'role',
                'phone',
                'document',
                'profile_image',
                'full_name',
                'birth_date',
                'start_date',
            ),
        }),
    )

    search_fields = (
        'username',
        'full_name',
        'email',
        'document',
    )


admin.site.register(Grupo)
admin.site.register(Curso)
admin.site.register(Enrollment)
admin.site.register(Material)
admin.site.register(Announcement)
admin.site.register(Assignment)
admin.site.register(Submission)
admin.site.register(Evaluation)
admin.site.register(EvaluationGrade)
admin.site.register(Attendance)