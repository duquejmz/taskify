# Taskify - API de Gestión de Tareas

API REST para gestión de tareas construida con FastAPI, SQLAlchemy y PostgreSQL.

## 🚀 Tecnologías

- **Python 3.11+**
- **FastAPI** - Framework web moderno y rápido
- **SQLAlchemy** - ORM para Python
- **PostgreSQL** - Base de datos relacional
- **Alembic** - Migraciones de base de datos
- **Argon2** - Hash seguro de contraseñas
- **JWT (python-jose)** - Autenticación basada en tokens
- **Pydantic** - Validación de datos

## ⚙️ Variables de Entorno

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

## 🐳 Levantar PostgreSQL con Docker

```bash
# Iniciar el contenedor de PostgreSQL
docker-compose up -d

# Verificar que está corriendo
docker ps
```

El archivo `docker-compose.yml` configura PostgreSQL con las credenciales definidas en `.env`.

## 🛠️ Instalación y Ejecución

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
python -c "from src.models.permission import Permission; from src.models.role import Role; from src.models.tag import Tag; from src.models.task import Task; from src.models.user import User; from src.db.session import SessionLocal; from src.db.seed import seed_initial_data; db = SessionLocal(); seed_initial_data(db); db.close(); print('Seed completado!')"
```

### 5. Iniciar el servidor

```bash
python -m uvicorn src.main:app --reload --port 8000
```

La API estará disponible en: http://localhost:8000

- Documentación Swagger: http://localhost:8000/docs
- Documentación ReDoc: http://localhost:8000/redoc

## 👤 Usuario Inicial

El seed crea automáticamente un usuario administrador:

| Campo | Valor |
|-------|-------|
| Email | `admin@test.com` |
| Password | `Admin123*` |
| Rol | `admin` |

## 📚 Endpoints de la API

### Autenticación

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/auth/login` | Iniciar sesión y obtener token JWT |

### Tareas (requieren autenticación)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/tasks` | Listar tareas (paginado) |
| POST | `/tasks` | Crear nueva tarea |
| GET | `/tasks/{id}` | Obtener tarea por ID |
| PATCH | `/tasks/{id}` | Actualizar tarea |
| DELETE | `/tasks/{id}` | Eliminar tarea |

## 🧪 Ejemplos de Uso (curl)

### Login

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@test.com", "password": "Admin123*"}'
```

Respuesta:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Crear Tarea

```bash
curl -X POST "http://localhost:8000/tasks" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <tu_token>" \
  -d '{
    "title": "Mi primera tarea",
    "description": "Descripción de la tarea",
    "status": "pending",
    "priority": "high"
  }'
```

### Listar Tareas (paginado)

```bash
curl -X GET "http://localhost:8000/tasks?page=1&page_size=10" \
  -H "Authorization: Bearer <tu_token>"
```

Respuesta:
```json
{
  "items": [...],
  "total": 1,
  "page": 1,
  "page_size": 10,
  "total_pages": 1
}
```

### Actualizar Tarea

```bash
curl -X PATCH "http://localhost:8000/tasks/<task_id>" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <tu_token>" \
  -d '{"status": "completed"}'
```

### Eliminar Tarea

```bash
curl -X DELETE "http://localhost:8000/tasks/<task_id>" \
  -H "Authorization: Bearer <tu_token>"
```

## 🗃️ Índices de Base de Datos

Se definieron índices en los siguientes campos para optimizar consultas frecuentes:

| Tabla | Índice | Justificación |
|-------|--------|---------------|
| `tasks` | `user_id + status` | Filtrar tareas por usuario y estado |
| `tasks` | `priority` | Filtrar por prioridad |
| `tasks` | `created_at` | Ordenamiento por fecha |
| `users` | `email` (unique) | Login por email |
| `users` | `username` (unique) | Búsqueda por username |
| `users` | `role_id` | Filtrar usuarios por rol |

## 🔒 Decisiones de Seguridad

1. **Argon2** para hash de contraseñas (recomendado sobre bcrypt por resistencia a ataques GPU)
2. **JWT** con expiración configurable (default: 30 minutos)
3. **Endpoints protegidos** - Todas las operaciones de tareas requieren autenticación
4. **Validación Pydantic** - Todos los inputs son validados automáticamente

## 📋 Manejo de Errores HTTP

| Código | Descripción |
|--------|-------------|
| 400 | Bad Request - Datos inválidos |
| 401 | Unauthorized - Token inválido o expirado |
| 404 | Not Found - Recurso no encontrado |
| 422 | Unprocessable Entity - Error de validación |
| 500 | Internal Server Error |

## 🔧 Trade-offs y Decisiones

1. **Identificación por email**: Se usa email para login (más común y user-friendly)
2. **Paginación offset-based**: Simple de implementar, suficiente para datasets pequeños/medianos
3. **Soft delete vs Hard delete**: Se implementó hard delete por simplicidad (en producción considerar soft delete)
4. **Tareas por usuario**: Cada usuario solo ve sus propias tareas (multi-tenant simple)

## 📝 Licencia

MIT