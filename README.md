# 🚀 Backend Python - FastAPI REST API

Backend profesional construido con **FastAPI**, **MongoDB** y **Redis** que implementa autenticación JWT, autorización por roles, rate limiting y caching.

---

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Stack Tecnológico](#-stack-tecnológico)
- [Arquitectura](#-arquitectura)
- [Flujo de Autenticación](#-flujo-de-autenticación)
- [Instalación](#-instalación)
- [Variables de Entorno](#-variables-de-entorno)
- [Endpoints Principales](#-endpoints-principales)
- [Estructura del Proyecto](#-estructura-del-proyecto)

---

## ✨ Características

### 🔐 Seguridad
- **Autenticación JWT** con tokens Bearer
- **Hashing de contraseñas** con Argon2
- **Autorización por roles** (Admin y User)
- **Rate Limiting** para prevenir ataques de fuerza bruta
- **Validaciones robustas** con Pydantic

### ⚡ Performance
- **Caching con Redis** (50x más rápido en consultas repetidas)
- **Consultas optimizadas** a MongoDB con proyecciones
- **Cache-Aside Pattern** para datos frecuentes

### 🛡️ Buenas Prácticas
- **Arquitectura por capas** (Routes → Services → Repositories)
- **Separación de responsabilidades**
- **Manejo centralizado de errores**
- **Configuración por variables de entorno**

---

## 🛠️ Stack Tecnológico

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| **Python** | 3.12+ | Lenguaje base |
| **FastAPI** | Latest | Framework web |
| **MongoDB** | 5.0+ | Base de datos NoSQL |
| **Redis** | 7.0+ | Cache en memoria |
| **PyMongo** | Latest | Driver MongoDB |
| **Pydantic** | v2 | Validación de datos |
| **PyJWT** | Latest | Tokens JWT |
| **pwdlib** | Latest | Hashing con Argon2 |

---

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                        CLIENTE                              │
│                    (Postman, Frontend)                      │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      ROUTES LAYER                           │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐   │
│  │ auth_routes  │  │ user_routes  │  │  Middlewares    │   │
│  │   (login)    │  │   (CRUD)     │  │ (rate_limiter)  │   │
│  └──────────────┘  └──────────────┘  └─────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                     SERVICES LAYER                          │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐   │
│  │ auth_service │  │ user_service │  │ Validaciones    │   │
│  │ (JWT logic)  │  │ (Business)   │  │  (Permisos)     │   │
│  └──────────────┘  └──────────────┘  └─────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   REPOSITORIES LAYER                        │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐   │
│  │auth_repository│  │user_repository│  │ cache_utilities│   │
│  │ (BD queries) │  │  (BD queries) │  │ (Redis ops)    │   │
│  └──────────────┘  └──────────────┘  └─────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            │
                ┌───────────┴───────────┐
                ▼                       ▼
         ┌──────────┐           ┌──────────┐
         │ MongoDB  │           │  Redis   │
         │(Datos)   │           │ (Cache)  │
         └──────────┘           └──────────┘
```

---

## 🔄 Flujo de Autenticación

### 1️⃣ Login
```
Cliente                Backend                  MongoDB                Redis
  │                       │                        │                      │
  │──POST /login─────────▶│                        │                      │
  │ {username, password}  │                        │                      │
  │                       │                        │                      │
  │                       │──Buscar usuario────────▶                      │
  │                       │                        │                      │
  │                       │◀─────Usuario───────────│                      │
  │                       │                        │                      │
  │                       │──Verificar password────│                      │
  │                       │   (Argon2)             │                      │
  │                       │                        │                      │
  │                       │──Generar JWT───────────│                      │
  │                       │   (30 min expiry)      │                      │
  │                       │                        │                      │
  │◀─{access_token}───────│                        │                      │
  │                       │                        │                      │
```

### 2️⃣ Request Autenticado con Cache
```
Cliente                Backend                  Redis                  MongoDB
  │                       │                        │                      │
  │──GET /users/123──────▶│                        │                      │
  │ Header: Bearer token  │                        │                      │
  │                       │                        │                      │
  │                       │──Validar JWT───────────│                      │
  │                       │                        │                      │
  │                       │──Buscar en cache───────▶                      │
  │                       │   key: "user:123"      │                      │
  │                       │                        │                      │
  │                       │◀────¿Existe?───────────│                      │
  │                       │                        │                      │
  │             ┌─────────┴─────────┐              │                      │
  │             │                   │              │                      │
  │         SÍ existe           NO existe          │                      │
  │             │                   │              │                      │
  │             │                   │──Consultar MongoDB───────────────────▶
  │             │                   │              │                      │
  │             │                   │◀────Usuario──────────────────────────│
  │             │                   │              │                      │
  │             │                   │──Guardar en cache────────▶          │
  │             │                   │   TTL: 1 hora│                      │
  │             │                   │              │                      │
  │             └───────────┬───────┘              │                      │
  │                         │                      │                      │
  │◀────Respuesta JSON──────│                      │                      │
  │  {id, name, email...}   │                      │                      │
  │                         │                      │                      │
```

---

## 📦 Instalación

### 1. Clonar repositorio
```bash
git clone <repository-url>
cd backend-py
```

### 2. Crear entorno virtual
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Iniciar MongoDB
```bash
# Asegúrate de tener MongoDB instalado y corriendo
mongod
```

### 5. Iniciar Redis
```bash
# Instalar Redis
sudo apt install redis-server  # Linux
brew install redis             # Mac

# Iniciar en puerto 6380
redis-server --port 6380
```

### 6. Configurar variables de entorno
Crea un archivo `.env` en la raíz del proyecto (ver sección siguiente).

### 7. Ejecutar la aplicación
```bash
python run.py
```

La API estará disponible en: **http://localhost:8000**

Documentación interactiva: **http://localhost:8000/docs**

---

## 🔧 Variables de Entorno

Crea un archivo `.env` y copiar el contenido de `.env.example` con tus valores personalizados:

```bash
# Configuration JWT
SECRET_KEY = your_secret_key_here
ACCESS_TOKEN_EXPIRE_MINUTES = your_expire_time_here
ALGORITHM = your_algorithm_here

# Configuration MongoDB
PASSWORD_MONGODB = your_mongodb_password_here
USERNAME_MONGODB = your_mongodb_username_here
DATABASE_NAME = your_database_name_here
URL_MONGO_DB = your_mongodb_url_here

# Configuration Redis
REDIS_HOST = your_redis_host_here
REDIS_PORT = your_redis_port_here
REDIS_DB = your_redis_db_here

CACHE_TTL_USER = your_cache_ttl_user_here  # Time to live for user cache
CACHE_TTL_LOGIN = your_cache_ttl_login_here  # Time to live for login cache
CACHE_TTL_USERS_LIST = your_cache_ttl_users_list_here  # Time to live for users list cache
```

---

## 📡 Endpoints Principales

### Autenticación

#### POST `/login`
Login de usuario y generación de JWT.

**Request:**
```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

### Usuarios

#### GET `/users`
Obtener lista de usuarios (requiere autenticación).

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
[
  {
    "id": "507f1f77bcf86cd799439011",
    "username": "juan",
    "email": "juan@mail.com",
    "role": "user"
  }
]
```

---

#### GET `/users/{id}`
Obtener usuario por ID (con cache).

**Permisos:**
- Admin: Puede ver cualquier usuario
- User: Solo puede ver su propio perfil

**Response:**
```json
{
  "id": "507f1f77bcf86cd799439011",
  "username": "juan",
  "email": "juan@mail.com",
  "role": "user",
  "created_at": "2026-04-27T10:30:00"
}
```

---

#### POST `/users`
Crear nuevo usuario (requiere rol admin).

**Request:**
```json
{
  "username": "maria",
  "email": "maria@mail.com",
  "password": "maria123",
  "role": "user"
}
```

---

#### PUT `/users/{id}`
Actualizar usuario existente.

**Permisos:**
- Admin: Puede actualizar cualquier usuario
- User: Solo puede actualizar su propio perfil

---

#### DELETE `/users/{id}`
Eliminar usuario (requiere rol admin).

---

#### PUT `/users/{id}/change-password`
Cambiar contraseña de usuario.

**Request:**
```json
{
  "current_password": "password_actual",
  "new_password": "password_nuevo"
}
```

---

## 📂 Estructura del Proyecto

```
backend-py/
│
├── app/
│   ├── config/
│   │   ├── __init__.py
│   │   ├── setting.py           # Variables de entorno
│   │   └── redis_config.py      # Configuración Redis
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   └── user_models.py       # Modelos Pydantic
│   │
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── auth_repository.py   # Queries autenticación
│   │   └── user_repository.py   # Queries usuarios
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth_routes.py       # Endpoints /login
│   │   └── user_routes.py       # Endpoints /users
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_services.py     # Lógica JWT
│   │   └── user_services.py     # Lógica de negocio
│   │
│   ├── utilities/
│   │   ├── __init__.py
│   │   ├── auth_utilities.py    # Rate limiter
│   │   ├── cache_utilities.py   # Funciones Redis
│   │   └── validation.py        # Validaciones
│   │
│   └── main.py                  # FastAPI app
│
├── .env                         # Variables de entorno
├── .gitignore
├── requirements.txt
├── run.py                       # Script de inicio
└── README.md
```

---

## 🔒 Seguridad Implementada

### ✅ Rate Limiting
- Máximo 5 requests por minuto por IP en `/login`
- Previene ataques de fuerza bruta

### ✅ Password Hashing
- Argon2 (algoritmo ganador Password Hashing Competition)
- Salt automático por usuario

### ✅ JWT Tokens
- Expiración de 30 minutos
- Firmados con clave secreta (HS256)

### ✅ Autorización por Roles
- Endpoints protegidos según rol (admin/user)
- Validación en capa de servicios

### ✅ Validaciones
- Pydantic valida todos los inputs
- Prevención de inyección MongoDB

---

## 🚀 Performance

### Caching con Redis

| Operación | Sin Cache | Con Cache | Mejora |
|-----------|-----------|-----------|--------|
| GET /users/{id} | ~50ms | ~1ms | **50x** ⚡ |
| GET /users (lista) | ~100ms | ~2ms | **50x** ⚡ |

### Cache-Aside Pattern

```
1. Primera request → MongoDB (50ms) → Cachea resultado
2. Segunda request → Redis (1ms) ⚡
3. Después de 1 hora → Cache expira → Vuelve a MongoDB
```

---

## 📝 Notas Importantes

### Base de Datos
- **MongoDB** debe estar corriendo en `localhost:27017`
- Se creará automáticamente la base de datos `myapp_db`

### Redis
- **Redis** debe estar corriendo en `localhost:6380`
- Si usas el puerto default `6379`, actualizar `.env`

### Primer Usuario
Para crear el primer usuario admin, usa la consola MongoDB:

```javascript
use myapp_db
db.users.insertOne({
  username: "admin",
  email: "admin@mail.com",
  password_hash: "$argon2id$...",  // Usar /login después de crear
  role: "admin",
  created_at: new Date()
})
```

O crea un usuario normal via API y luego actualiza su rol a "admin" en MongoDB.

---

## 📄 Licencia

Este proyecto es de uso educativo.

---

## 👨‍💻 Autor

**Leandro Aquiro**  
Proyecto de aprendizaje - Backend con Python y FastAPI

---

**Fecha de creación:** Abril 2026  
