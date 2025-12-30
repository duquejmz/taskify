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

## Instalación y Ejecución

### 1. Clonar e instalar dependencias

```bash
# Crear entorno virtual (opcional pero recomendado)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o en Windows:
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Levantar la base de datos

```bash
docker-compose up -d
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



## Variables de Entorno

Crear un archivo `.env` en la raíz del proyecto:

```env
# Base de datos
DB_HOST=localhost
DB_PORT=5432
DB_NAME=technical_test
DB_USER=postgres
DB_PASSWORD=postgres
DB_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/technical_test

# JWT
JWT_SECRET_KEY=tu-clave-secreta-muy-segura-cambiar-en-produccion
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=30
```

## Levantar PostgreSQL con Docker

```bash
# Iniciar el contenedor de PostgreSQL
docker-compose up -d

# Verificar que está corriendo
docker ps
```

El archivo `docker-compose.yml` configura PostgreSQL con las credenciales definidas en `.env`.

## Usuario Inicial

El seed crea automáticamente un usuario administrador:

| Campo | Valor |
|-------|-------|
| Email | `admin@test.com` |
| Username | `admin` |
| Password | `Admin123!` |
| Rol | `admin` |

## Ejemplos de Uso

### Login (por email o username)

```bash
# Por email
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"identifier": "admin@test.com", "password": "Admin123!"}'

# Por username
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"identifier": "admin", "password": "Admin123!"}'
```

Respuesta:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Crear Tarea (con tags automáticos)

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

### Listar Tareas (con filtros)

```bash
# Paginación básica
curl -X GET "http://localhost:8000/api/v1/tasks?page=1&page_size=10" \
  -H "Authorization: Bearer <tu_token>"

# Con filtros
curl -X GET "http://localhost:8000/api/v1/tasks?status=pending&priority=high" \
  -H "Authorization: Bearer <tu_token>"
```

### Crear Usuario (Admin)

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

### Desactivar Usuario (Admin)

```bash
curl -X PATCH "http://localhost:8000/api/v1/users/<user_id>/deactivate" \
  -H "Authorization: Bearer <tu_token>"
```

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

| Tabla | Índice | Justificación |
|-------|--------|---------------|
| `tasks` | `user_id + status` | Filtrar tareas por usuario y estado |
| `tasks` | `priority` | Filtrar por prioridad |
| `tasks` | `created_at` | Ordenamiento por fecha |
| `users` | `email` (unique) | Login por email |
| `users` | `username` (unique) | Login por username |
| `users` | `role_id` | Filtrar usuarios por rol |
| `tags` | `name` (unique) | Búsqueda por nombre |

## Manejo de Errores HTTP

| Código | Descripción | Ejemplo |
|--------|-------------|---------|
| 400 | Bad Request | Datos de entrada mal formados |
| 401 | Unauthorized | Token inválido, expirado o no proporcionado |
| 403 | Forbidden | Usuario sin permisos de administrador |
| 404 | Not Found | Recurso no encontrado |
| 409 | Conflict | Email, username, tag o rol ya existe |
| 422 | Unprocessable Entity | Validación de negocio fallida |

## Decisiones de Seguridad

1. **Argon2** para hash de contraseñas (resistente a ataques GPU)
2. **JWT** con expiración configurable (default: 30 minutos)
3. **Endpoints protegidos** por rol (Usuario o Admin)
4. **Validación Pydantic** en todos los inputs
5. **Soft delete** para usuarios (desactivación en lugar de eliminación)

## Características Especiales

1. **Login flexible**: Acepta email O username como identificador
2. **Auto-creación de tags**: Al crear/actualizar tareas, los tags se crean si no existen
3. **Filtrado de usuarios inactivos**: Por defecto, los endpoints de listado solo muestran usuarios activos
4. **Paginación consistente**: Todos los endpoints de listado soportan `page` y `page_size`. Se implementa utilizando offset based.
5. **Permisos**: Solo el administrador, puede realizar la mayoria de acciones de edición.
6. **Campos de auditoria**: Implementar campos de auditoria para tner un mejor control de cuando y quien crea y poder filtrar por estos.

