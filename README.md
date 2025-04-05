# Airport API Service

REST API service for managing airport operations, including flights, tickets, and user management.

## Super user credentials
- email: `admin@admin.com`
- password: `123`

## Features
- JWT Authentication
- Admin panel
- Documentation with Swagger/OpenAPI
- Docker containerization
- PostgreSQL database

## Project Structure

airport_service/

├── airport/ `# Main application`

│ ├── migrations/

│ ├── models.py `# Database models`

│ ├── serializers.py `# DRF serializers`

│ ├── views.py `# API views`

│ ├── urls.py `# URL routing`

│ └── permissions.py `# Custom permissions`


├── user/ `# User management app`

│ ├── migrations/

│ ├── models.py `# Custom user model`

│ ├── serializers.py `# User serializers`

│ └── urls.py `# User URLs`


├── airport_service/ `# Project configuration`

│ ├── settings.py `# Project settings`

│ └── urls.py `# Main URL routing`



## Installation and Setup

### Prerequisites
- Docker and Docker Compose installed
- Git installed

### Getting Started

1. Clone the repository:
```bash
docker pull nrjss67/airpotapiproject:latest
```

2. Create `.env` file in the root directory:
```env
POSTGRES_PASSWORD=airport
POSTGRES_USER=airport
POSTGRES_DB=airport
POSTGRES_HOST=db
POSTGRES_PORT=5432
PGDATA=/var/lib/postgresql/data
```

3. Build and run Docker containers:
```bash
docker-compose up --build
```

The API will be available at `http://localhost:8000/`
Admin panel: `http://localhost:8000/admin/`
API documentation: `http://localhost:8000/api/doc/swagger/`

### Docker Commands

- Start containers: `docker-compose up`
- Stop containers: `docker-compose down`
- Remove volumes: `docker-compose down -v`
- View logs: `docker-compose logs`
- Access container shell: `docker-compose exec app sh`

## API Endpoints

Airport API:
- `/api/v1/user/` - User management
- `/api/v1/airport/airplane-type/` - Airplane types
- `/api/v1/airport/airplane/` - Airplanes
- `/api/v1/airport/airport/` - Airports
- `/api/v1/airport/crew/` - Crew management
- `/api/v1/airport/route/` - Flight routes
- `/api/v1/airport/flight/` - Flights
- `/api/v1/airport/order/` - Orders
- `/api/v1/airport/ticket/` - Tickets

User API:
- `/api/v1/user/token/` - Login
- `/api/v1/user/token/refresh/` - Register

Documentation:
- `/api/v1/doc/swagger/` - Swagger UI

## Working with GitHub

1. Create a new branch for features:
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes and commit:
```bash
git add .
git commit -m "Description of changes"
```

3. Push changes to GitHub:
```bash
git push origin feature/your-feature-name
```

4. Create a Pull Request on GitHub

5. After review and approval, merge into main branch

### Branch Strategy
- `main` - production code
- `dev` - development branch
- `feature/*` - new features
- `bugfix/*` - bug fixes

## Technologies Used
- Python 3.11
- Django 5.1.7
- Django REST Framework
- PostgreSQL
- Docker
- JWT Authentication
- Swagger/OpenAPI

## Development

To make migrations:
```bash
docker-compose exec app python manage.py makemigrations
docker-compose exec app python manage.py migrate
```

## Contributing
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

