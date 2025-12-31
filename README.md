# Taskify - API de Gestión de Tareas

API REST para gestión de tareas construida con FastAPI, SQLAlchemy y PostgreSQL.

## Tecnologías

- **Python 3.11+**
- **FastAPI** - Framework web moderno y rápido
- **SQLAlchemy** - ORM para Python
- **PostgreSQL** - Base de datos relacional
- **Alembic** - Migraciones de base de datos
- **Argon2** - Hash seguro de contraseñas
- **JWT (python-jose)** - Autenticación basada en tokens
- **Pydantic** - Validación de datos

## Variables de Entorno

Crear un archivo `.env` en la raíz del proyecto

## Levantar PostgreSQL con Docker

```bash
# Iniciar el contenedor de PostgreSQL
docker-compose up -d

# Verificar que está corriendo
docker ps
```

El archivo `docker-compose.yml` configura PostgreSQL con las credenciales definidas en `.env`.

## Instalación y Ejecución

### 1. Clonar e instalar dependencias

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Para Linux/Mac
source venv/bin/activate  
# Para Windows:
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Levantar la base de datos

```bash
docker compose up -d
```

### 3. Ejecutar migraciones

```bash
python -m alembic upgrade head
```

### 4. Cargar datos iniciales (seed)

```bash
python -c "from src.db.session import SessionLocal; from src.db.seed import seed_initial_data; db = SessionLocal(); seed_initial_data(db); db.close(); print('Seed completado!')"
```

### 5. Iniciar el servidor

```bash
python -m uvicorn src.main:app --reload --port 8000
```

La API estará disponible en: http://localhost:8000

- Documentación Swagger: http://localhost:8000/docs
- Documentación ReDoc: http://localhost:8000/redoc

## Usuario Inicial

El seed crea automáticamente un usuario administrador:

| Campo | Valor |
|-------|-------|
| Email | `admin@test.com` |
| Username | `admin` |
| Password | `Admin123!` |
| Rol | `admin` |

## Ejemplos de Uso

> **Nota**: Reemplaza `<tu_token>` con el token JWT obtenido del login.

---

## Autenticación

### Login (por email o username)

```bash
# Por email
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@test.com", "password": "Admin123*"}'

# Por username
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "Admin123*"}'
```

**Respuesta:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

## CRUD de Tareas

### Crear Tarea

```bash
curl -X POST "http://localhost:8000/api/v1/tasks" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <tu_token>" \
  -d '{
    "title": "Mi primera tarea",
    "description": "Descripción de la tarea",
    "status": "pending",
    "priority": "high",
    "tag_names": ["backend", "urgente"]
  }'
```

> **Nota**: Si los tags no existen, se crean automáticamente.

**Valores permitidos:**
- `status`: `pending`, `in_progress`, `completed`
- `priority`: `low`, `medium`, `high`

### Listar Tareas (con paginación y filtros)

```bash
# Paginación básica
curl -X GET "http://localhost:8000/api/v1/tasks?page=1&page_size=10" \
  -H "Authorization: Bearer <tu_token>"

# Con filtros por estado
curl -X GET "http://localhost:8000/api/v1/tasks?status=pending" \
  -H "Authorization: Bearer <tu_token>"

# Con filtros por prioridad
curl -X GET "http://localhost:8000/api/v1/tasks?priority=high" \
  -H "Authorization: Bearer <tu_token>"

# Combinando filtros
curl -X GET "http://localhost:8000/api/v1/tasks?status=pending&priority=high&page=1&page_size=5" \
  -H "Authorization: Bearer <tu_token>"
```

**Respuesta:**
```json
{
  "items": [
    {
      "id": "uuid",
      "title": "Mi tarea",
      "description": "Descripción",
      "status": "pending",
      "priority": "high",
      "tags": [{"id": "uuid", "name": "backend"}],
      "created_at": "2025-12-30T10:00:00",
      "updated_at": "2025-12-30T10:00:00"
    }
  ],
  "total": 1,
  "page": 1,
  "page_size": 10,
  "total_pages": 1
}
```

### Obtener Tarea por ID

```bash
curl -X GET "http://localhost:8000/api/v1/tasks/<task_id>" \
  -H "Authorization: Bearer <tu_token>"
```

### Actualizar Tarea

```bash
curl -X PATCH "http://localhost:8000/api/v1/tasks/<task_id>" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <tu_token>" \
  -d '{
    "title": "Tarea actualizada",
    "status": "in_progress",
    "priority": "medium"
  }'
```

> **Nota**: Solo se actualizan los campos proporcionados.

### Eliminar Tarea

```bash
curl -X DELETE "http://localhost:8000/api/v1/tasks/<task_id>" \
  -H "Authorization: Bearer <tu_token>"
```

---

## CRUD de Usuarios (Solo Admin)

### Crear Usuario

```bash
curl -X POST "http://localhost:8000/api/v1/users" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <tu_token>" \
  -d '{
    "name": "Juan Pérez",
    "username": "juanperez",
    "email": "juan@example.com",
    "password": "Password123!",
    "role_name": "user"
  }'
```

### Listar Usuarios

```bash
# Listar usuarios activos (default)
curl -X GET "http://localhost:8000/api/v1/users?page=1&page_size=10" \
  -H "Authorization: Bearer <tu_token>"

# Listar usuarios inactivos
curl -X GET "http://localhost:8000/api/v1/users?is_active=false" \
  -H "Authorization: Bearer <tu_token>"

# Listar todos los usuarios (activos e inactivos)
curl -X GET "http://localhost:8000/api/v1/users?is_active=" \
  -H "Authorization: Bearer <tu_token>"
```

**Respuesta:**
```json
{
  "items": [
    {
      "id": "uuid",
      "name": "Admin User",
      "username": "admin",
      "email": "admin@test.com",
      "is_active": true,
      "role": {"id": "uuid", "name": "admin"},
      "created_at": "2025-12-30T10:00:00"
    }
  ],
  "total": 1,
  "page": 1,
  "page_size": 10,
  "total_pages": 1
}
```

### Cambiar Estado de Usuario (Activar/Desactivar)

```bash
# Desactivar usuario
curl -X PATCH "http://localhost:8000/api/v1/users/<user_id>/status?is_active=false" \
  -H "Authorization: Bearer <tu_token>"

# Activar usuario
curl -X PATCH "http://localhost:8000/api/v1/users/<user_id>/status?is_active=true" \
  -H "Authorization: Bearer <tu_token>"
```

> **Nota**: No puedes desactivar tu propia cuenta de administrador.

---

## CRUD de Roles (Solo Admin)

### Crear Rol

```bash
curl -X POST "http://localhost:8000/api/v1/roles" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <tu_token>" \
  -d '{
    "name": "moderator",
    "description": "Rol de moderador con permisos limitados"
  }'
```

### Listar Roles

```bash
curl -X GET "http://localhost:8000/api/v1/roles" \
  -H "Authorization: Bearer <tu_token>"
```

**Respuesta:**
```json
{
  "items": [
    {
      "id": "uuid",
      "name": "admin",
      "description": "Administrador del sistema",
      "created_at": "2025-12-30T10:00:00"
    },
    {
      "id": "uuid",
      "name": "user",
      "description": "Usuario estándar",
      "created_at": "2025-12-30T10:00:00"
    }
  ],
  "total": 2
}
```

### Obtener Rol con sus Permisos

```bash
curl -X GET "http://localhost:8000/api/v1/roles/<role_id>" \
  -H "Authorization: Bearer <tu_token>"
```

**Respuesta:**
```json
{
  "id": "uuid",
  "name": "admin",
  "description": "Administrador del sistema",
  "permissions": [
    {"id": "uuid", "name": "create_user"},
    {"id": "uuid", "name": "delete_user"}
  ],
  "created_at": "2025-12-30T10:00:00"
}
```

### Actualizar Permisos de un Rol (Agregar/Quitar)

```bash
# Agregar permisos
curl -X PATCH "http://localhost:8000/api/v1/roles/<role_id>/permissions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <tu_token>" \
  -d '{
    "add": ["create_task", "edit_task"]
  }'

# Quitar permisos
curl -X PATCH "http://localhost:8000/api/v1/roles/<role_id>/permissions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <tu_token>" \
  -d '{
    "remove": ["delete_task"]
  }'

# Agregar y quitar en una sola petición
curl -X PATCH "http://localhost:8000/api/v1/roles/<role_id>/permissions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <tu_token>" \
  -d '{
    "add": ["create_task", "update_task"],
    "remove": ["delete_task"]
  }'
```

> **Nota**: Se pueden enviar ambos campos (`add` y `remove`) o solo uno de ellos.

### Obtener Usuarios por Rol

```bash
curl -X GET "http://localhost:8000/api/v1/roles/admin/users?page=1&page_size=10" \
  -H "Authorization: Bearer <tu_token>"

# Filtrar por estado activo
curl -X GET "http://localhost:8000/api/v1/roles/user/users?is_active=true" \
  -H "Authorization: Bearer <tu_token>"
```

---

## CRUD de Permisos (Solo Admin)

### Crear Permiso

```bash
curl -X POST "http://localhost:8000/api/v1/permissions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <tu_token>" \
  -d '{
    "name": "export_reports",
    "description": "Permite exportar reportes del sistema"
  }'
```

### Listar Permisos

```bash
curl -X GET "http://localhost:8000/api/v1/permissions" \
  -H "Authorization: Bearer <tu_token>"
```

**Respuesta:**
```json
{
  "items": [
    {
      "id": "uuid",
      "name": "create_task",
      "description": "Permite crear tareas",
      "created_at": "2025-12-30T10:00:00"
    },
    {
      "id": "uuid",
      "name": "delete_user",
      "description": "Permite eliminar usuarios",
      "created_at": "2025-12-30T10:00:00"
    }
  ],
  "total": 2
}
```

---

## CRUD de Tags

### Crear Tag (Solo Admin)

```bash
curl -X POST "http://localhost:8000/api/v1/tags" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <tu_token>" \
  -d '{
    "name": "importante"
  }'
```

### Listar Tags

```bash
curl -X GET "http://localhost:8000/api/v1/tags" \
  -H "Authorization: Bearer <tu_token>"
```

**Respuesta:**
```json
{
  "items": [
    {
      "id": "uuid",
      "name": "backend",
      "created_at": "2025-12-30T10:00:00"
    },
    {
      "id": "uuid",
      "name": "urgente",
      "created_at": "2025-12-30T10:00:00"
    }
  ],
  "total": 2
}
```

### Obtener Tareas por Tag

```bash
curl -X GET "http://localhost:8000/api/v1/tags/backend/tasks" \
  -H "Authorization: Bearer <tu_token>"
```

**Respuesta:**
```json
[
  {
    "id": "uuid",
    "title": "Implementar API",
    "description": "Crear endpoints REST",
    "status": "in_progress",
    "priority": "high",
    "tags": [{"id": "uuid", "name": "backend"}],
    "created_at": "2025-12-30T10:00:00"
  }
]
```

---



## Modelo de Datos

### Relaciones

- **User ↔ Role**: N:1 (cada usuario tiene un rol)
- **User ↔ Task**: 1:N (un usuario tiene muchas tareas)
- **Task ↔ Tag**: M:N (tabla intermedia `task_tag`)
- **Role ↔ Permission**: M:N (tabla intermedia `permission_role`)

### Campos de Auditoría

Todos los modelos incluyen:
- `created_at`: Fecha de creación
- `created_by`: ID del usuario que creó el registro
- `updated_at`: Fecha de última actualización
- `updated_by`: ID del usuario que actualizó el registro

## Índices de Base de Datos

Los índices fueron diseñados para optimizar las consultas más frecuentes de la aplicación, reduciendo el tiempo de respuesta y mejorando el rendimiento general del sistema.


| Tabla | Índice | Justificación |
|-------|--------|---------------|
| `tasks` | `user_id + status` | Optimiza la consulta principal del dashboard: obtener tareas de un usuario filtradas por estado. Al ser un índice compuesto, evita escaneos completos de tabla cuando se aplican ambos filtros simultáneamente. |
| `tasks` | `priority` | Acelera el filtrado por prioridad, consulta frecuente para mostrar tareas urgentes o de alta prioridad. |
| `tasks` | `created_at` | Mejora el rendimiento del ordenamiento cronológico, operación común en listados paginados y reportes. |
| `users` | `email` (unique) | Garantiza unicidad y optimiza la autenticación por email, operación ejecutada en cada login. |
| `users` | `username` (unique) | Garantiza unicidad y optimiza la autenticación por username como método alternativo de login. |
| `users` | `role_id` | Acelera las consultas de usuarios por rol, útil para la gestión administrativa y filtros de permisos. |
| `tags` | `name` (unique) | Garantiza unicidad y optimiza la búsqueda de tags por nombre, operación frecuente al crear/editar tareas. |


## Manejo de Errores HTTP
Se implementó un manejo de errores estandarizado siguiendo las convenciones HTTP REST. Esto permite a los clientes de la API identificar y manejar errores de forma predecible, reduciendo el tiempo de debugging y mejorando la experiencia del desarrollador.

| Código | Descripción | Ejemplo |
|--------|-------------|---------|
| 400 | Bad Request | Datos de entrada mal formados |
| 401 | Unauthorized | Token inválido, expirado o no proporcionado |
| 403 | Forbidden | Usuario sin permisos de administrador |
| 404 | Not Found | Recurso no encontrado |
| 409 | Conflict | Email, username, tag o rol ya existe |
| 422 | Unprocessable Entity | Validación de negocio fallida |

**Nota**: La diferencia entre 400 y 422 es importante: 400 indica un problema de formato/sintaxis, mientras que 422 indica que los datos son válidos pero no cumplen las reglas de negocio (ej: intentar desactivar tu propia cuenta).

## Decisiones de Seguridad

Se priorizó la seguridad desde el diseño, implementando múltiples capas de protección para datos sensibles y acceso a recursos.

| Medida | Implementación | Justificación |
|--------|----------------|---------------|
| **Hash de contraseñas** | Argon2 | Resistente a ataques de fuerza bruta con GPU/ASIC por su alto consumo de memoria. |
| **Autenticación** | JWT con expiración | Tokens stateless que reducen carga en servidor. Expiración de 60 min limita ventana de ataque si un token es comprometido. |
| **Autorización** | Roles (User/Admin) | Control de acceso basado en roles (RBAC) que simplifica la gestión de permisos y cumple el principio de mínimo privilegio. |
| **Validación de entrada** | Pydantic | Validación estricta de tipos y formatos en cada request, previniendo inyecciones y datos malformados antes de llegar a la lógica de negocio. |
| **Eliminación de usuarios** | Soft delete | Desactivación en lugar de eliminación física, preservando integridad referencial y permitiendo auditoría histórica. |
| **Contraseñas seguras** | Validación de complejidad | Mínimo 8 caracteres, mayúscula, minúscula, número y carácter especial para prevenir contraseñas débiles. |


## Características Especiales

Funcionalidades adicionales implementadas para mejorar la experiencia de desarrollo y uso de la API.

| Característica | Descripción | Beneficio |
|----------------|-------------|-----------|
| **Login flexible** | Acepta email o username como identificador de autenticación | Mayor comodidad para el usuario, quien puede elegir su método preferido de acceso. |
| **Auto-creación de tags** | Al crear o actualizar tareas, los tags inexistentes se crean automáticamente | Simplifica el flujo de trabajo eliminando la necesidad de crear tags previamente. |
| **Filtrado de usuarios inactivos** | Los endpoints de listado muestran solo usuarios activos por defecto | Evita mostrar cuentas deshabilitadas, manteniendo listas limpias y relevantes. |
| **Paginación consistente** | Todos los endpoints de listado soportan `page` y `page_size` usando offset-based pagination | Permite manejar grandes volúmenes de datos de forma eficiente y predecible. |
| **Control de acceso por rol** | Solo administradores pueden gestionar usuarios, roles y permisos | Cumple el principio de mínimo privilegio, protegiendo operaciones sensibles. |
| **Campos de auditoría** | Todos los modelos incluyen `created_at`, `created_by`, `updated_at` y `updated_by` | Trazabilidad completa de cambios para debugging, auditorías y cumplimiento normativo. |

