# Práctica de Django REST Framework

Proyecto de aprendizaje basado en el tutorial oficial de Django REST Framework (DRF). Incluye la aplicación de inicio rápido (`quickstart`), una API básica de productos y el ejercicio de serializadores con snippets de código.

## Tecnologías

- Python 3
- Django 6.0.7
- Django REST Framework 3.17.1
- Pygments 2.20.0 (para resaltado de sintaxis en snippets)
- SQLite (base de datos por defecto)

## Requisitos

- Python 3.10 o superior
- `pip` actualizado
- Docker y Docker Compose (opcional, para ejecutar con contenedores)

## Instalación

1. Clonar el repositorio:

```bash
git clone <url-del-repositorio>
cd DRF-tutorial
```

2. Crear y activar el entorno virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Instalar las dependencias:

```bash
pip install -r requirements.txt
```

4. Aplicar las migraciones:

```bash
python manage.py migrate
```

5. Iniciar el servidor de desarrollo:

```bash
python manage.py runserver
```

La aplicación estará disponible en `http://127.0.0.1:8000/`.

### Opción 2: con Docker (recomendado para desarrollo)

1. Construir la imagen:

```bash
docker compose build
```

2. Levantar el contenedor:

```bash
docker compose up -d
```

El contenedor aplica las migraciones automáticamente y expone la aplicación en `http://127.0.0.1:8000/`.

3. Ver logs:

```bash
docker compose logs -f
```

4. Detener el entorno:

```bash
docker compose down
```

> El volumen `.:/app` en `docker-compose.yml` monta el código fuente local dentro del contenedor, por lo que los cambios que hagas en el código se reflejan inmediatamente gracias al recargador de Django (`StatReloader`).

## Estructura del proyecto

```
DRF-tutorial/
├── apps/                       # Aplicaciones del proyecto
│   ├── products/               # API de productos
│   └── snippets/               # Ejercicio de serializadores
├── tutorial/                   # Módulo de configuración del proyecto
│   ├── quickstart/             # App de inicio rápido de DRF
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py / asgi.py
├── Dockerfile                  # Imagen base de la aplicación
├── docker-compose.yml          # Orquestación del entorno de desarrollo
├── .dockerignore               # Archivos ignorados por Docker
├── manage.py
├── requirements.txt
├── makefile
├── db.sqlite3
└── snippet-exercise.md         # Guía del ejercicio de snippets
```

## Aplicaciones

### `tutorial.quickstart`

App del quickstart oficial de DRF. Expone endpoints de lectura/escritura sobre los modelos `User` y `Group` de Django, protegidos con autenticación.

### `apps.products`

API REST completa para gestionar productos. Utiliza un `ModelViewSet` y un `ModelSerializer`, con las siguientes operaciones:

- Listar productos
- Crear producto
- Obtener producto por ID
- Actualizar producto
- Eliminar producto

### `apps.snippets`

App del tutorial de serializadores de DRF. Contiene el modelo `Snippet` y dos serializadores (`SnippetSerializer` y `SnippetModelSerializer`). La guía de ejercicios se encuentra en `snippet-exercise.md`.

## Endpoints disponibles

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET / POST | `/` | Raíz de la API (router del quickstart) |
| GET / POST | `/api/products` | Listar / crear productos |
| GET / PUT / PATCH / DELETE | `/api/products/<id>` | Detalle, actualizar o eliminar un producto |
| GET / POST | `/users/` | Listar / crear usuarios (requiere autenticación) |
| GET / POST | `/groups/` | Listar / crear grupos (requiere autenticación) |
| GET / POST | `/api-auth/login/` | URLs de autenticación de DRF |

> Nota: el endpoint `/` actualmente expone las rutas del `quickstart` (`/users/` y `/groups/`). `apps.snippets` aún no tiene URLs registradas en el proyecto; se integra como parte del ejercicio de `snippet-exercise.md`.

## Comandos útiles

El proyecto incluye un `makefile` con comandos frecuentes:

```bash
# Crear el entorno virtual
make create

# Ver mensaje de activación del entorno virtual
make active

# Instalar dependencias
make install-requirements

# Guardar dependencias actuales
make save-requirements

# Aplicar migraciones
make migrate

# Crear un superusuario
make create-admin

# Iniciar el servidor de desarrollo
make run-server

# Abrir el shell de Django
make shell
```

## Ejercicio de snippets

Para seguir el tutorial de serializadores, consulta el archivo `snippet-exercise.md`. Allí encontrarás los pasos para:

- Trabajar con serializadores en el shell de Django.
- Refactorizar de `Serializer` a `ModelSerializer`.
- Crear vistas Django tradicionales que devuelvan JSON.
- Probar la API con `curl` o `HTTPie`.

## Notas

- El proyecto usa `APPEND_SLASH = False` en `tutorial/settings.py`.
- La paginación está configurada con `PageNumberPagination` y un tamaño de página de 10 elementos.
- Las carpetas `__pycache__/` están ignoradas en `.gitignore`.
- `ALLOWED_HOSTS` se configura mediante la variable de entorno `ALLOWED_HOSTS` (por defecto `*` para desarrollo local y contenedores).
- En el entorno Docker de desarrollo, el código se monta como volumen, por lo que no es necesario reconstruir la imagen al modificar archivos.

## Licencia

Este proyecto es de uso educativo.
