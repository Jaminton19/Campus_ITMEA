CAMPUS ITMEA - VERSION COMPLETA

1. Haga copia de seguridad de db.sqlite3 antes de reemplazar archivos.
2. Reemplace el contenido del proyecto por esta carpeta, conservando db.sqlite3 y media/.
3. Active el entorno virtual.
4. Ejecute: python manage.py migrate
5. Ejecute: python manage.py check
6. Ejecute: python manage.py runserver

IMPORTANTE: no ejecute makemigrations. Ya se incluye users/migrations/0004_campus.py.

Roles:
- admin: panel administrativo
- teacher: panel docente
- student: panel estudiante

Funciones incluidas:
- usuarios y roles
- grupos
- cursos y asignación de docente
- matrículas
- materiales y archivos
- anuncios
- tareas y entregas
- evaluaciones y calificaciones
- asistencia
- reportes básicos
