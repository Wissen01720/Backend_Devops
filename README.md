# Task Management API

A modern REST API built with FastAPI and PostgreSQL for managing tasks. Features automatic database initialization, async operations, and comprehensive API documentation.

## ✨ Features

- 🚀 **Fast & Modern**: Built with FastAPI and async SQLAlchemy
- 🗄️ **PostgreSQL Database**: Automatic table creation on startup (Supabase compatible)
- 📝 **Full CRUD Operations**: Create, Read, Update, Delete tasks
- 🔄 **Async/Await**: Non-blocking database operations
- 📚 **Auto Documentation**: Interactive Swagger UI and ReDoc
- 🐳 **Docker Ready**: Containerized with Docker and Docker Compose
- ✅ **Data Validation**: Pydantic models for request/response validation
- 🌐 **CORS Enabled**: Ready for frontend integration
- 💾 **Fallback Storage**: In-memory storage if database is not configured

## 🛠️ Tech Stack

- **FastAPI** - Modern web framework for building APIs
- **SQLAlchemy 2.0** - ORM with async support
- **AsyncPG** - Async PostgreSQL driver
- **Pydantic** - Data validation and settings management
- **Uvicorn** - ASGI server
- **PostgreSQL** - Database (Supabase)
- **Docker** - Containerization

## 📋 Prerequisites

- Python 3.11+ (for local development)
- PostgreSQL database or Supabase account
- Docker (optional, for containerized deployment)

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone <repository-url>
cd backend
```

### 2. Set up environment variables

Create a `.env` file from the example:

```bash
cp .env.example .env
```

Edit `.env` and add your database URL:

```env
DATABASE_URL="postgresql://user:password@host:5432/database"
```

> **Note**: If you don't configure `DATABASE_URL`, the app will use in-memory storage (data will be lost on restart).

### 3. Install dependencies

```bash
# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### 4. Run the application

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## 🐳 Docker Deployment

### Using Docker Compose

```bash
docker-compose up --build
```

### Using Docker directly

```bash
# Build image
docker build -t task-api .

# Run container
docker run -p 8000:8000 \
  -e DATABASE_URL="postgresql://..." \
  task-api
```

## 📖 API Documentation

Once the server is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 🔌 API Endpoints

### Health Check

```http
GET /health
```

Returns API status and task count.

### Tasks

#### Get all tasks

```http
GET /tasks
```

#### Create a task

```http
POST /tasks
Content-Type: application/json

{
  "title": "Task title",
  "description": "Task description (optional)"
}
```

#### Get a specific task

```http
GET /tasks/{task_id}
```

#### Update a task

```http
PUT /tasks/{task_id}
Content-Type: application/json

{
  "title": "Updated title",
  "description": "Updated description",
  "completed": true
}
```

#### Delete a task

```http
DELETE /tasks/{task_id}
```

## 💻 Usage Examples

### Using curl

```bash
# Health check
curl http://localhost:8000/health

# Create a task
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Learn FastAPI","description":"Complete the tutorial"}'

# Get all tasks
curl http://localhost:8000/tasks

# Update a task
curl -X PUT http://localhost:8000/tasks/{task_id} \
  -H "Content-Type: application/json" \
  -d '{"completed":true}'

# Delete a task
curl -X DELETE http://localhost:8000/tasks/{task_id}
```

### Using Python requests

```python
import requests

# Create a task
response = requests.post(
    "http://localhost:8000/tasks",
    json={"title": "My Task", "description": "Task details"}
)
task = response.json()
print(f"Created task: {task['id']}")

# Get all tasks
response = requests.get("http://localhost:8000/tasks")
tasks = response.json()
print(f"Total tasks: {len(tasks)}")
```

## 📁 Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py           # API route definitions
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py           # Application settings
│   │   └── database.py         # Database adapters (PostgreSQL/In-Memory)
│   └── models/
│       ├── __init__.py
│       ├── task.py             # Pydantic models (API schemas)
│       └── db_models.py        # SQLAlchemy models (ORM)
├── .env                        # Environment variables (not in git)
├── .env.example                # Environment variables template
├── .gitignore                  # Git ignore rules
├── .dockerignore               # Docker ignore rules
├── Dockerfile                  # Docker image definition
├── docker-compose.yml          # Docker Compose configuration
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🗄️ Database Schema

### Tasks Table

| Column      | Type                     | Description                        |
| ----------- | ------------------------ | ---------------------------------- |
| id          | UUID                     | Primary key (auto-generated)       |
| title       | VARCHAR(200)             | Task title (required)              |
| description | TEXT                     | Task description (optional)        |
| completed   | BOOLEAN                  | Completion status (default: false) |
| created_at  | TIMESTAMP WITH TIME ZONE | Creation timestamp (auto)          |

The table is created automatically when the application starts if it doesn't exist.

## ⚙️ Configuration

Configuration is managed through environment variables. Available options:

| Variable     | Description                  | Default               |
| ------------ | ---------------------------- | --------------------- |
| DATABASE_URL | PostgreSQL connection string | None (uses in-memory) |
| HOST         | Server host                  | 0.0.0.0               |
| PORT         | Server port                  | 8000                  |

## 🔒 Security Notes

- **Never commit `.env` file** (already in `.gitignore`)
- Use environment variables or secrets manager in production
- Keep database credentials secure
- Update dependencies regularly for security patches

## 🧪 Testing the API

### Automated Testing

The database automatically initializes on startup. You'll see:

```
✅ Base de datos PostgreSQL inicializada
INFO:     Application startup complete.
```

### Manual Testing

Visit the interactive documentation at `http://localhost:8000/docs` to test all endpoints directly in your browser.

## 🚧 Roadmap

- [x] PostgreSQL database integration
- [x] Automatic table creation
- [x] Full CRUD operations
- [x] Docker support
- [ ] Authentication (JWT)
- [ ] Unit and integration tests
- [ ] Rate limiting
- [ ] Pagination and filtering
- [ ] Database migrations (Alembic)

## 📝 Development

### Adding New Features

1. Define models in `app/models/`
2. Add database models in `app/models/db_models.py`
3. Create API routes in `app/api/routes.py`
4. Update documentation

### Code Style

- Follow PEP 8 guidelines
- Use type hints
- Add docstrings to functions
- Keep functions small and focused

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

DevOps Student - Universidad

## 🙏 Acknowledgments

- FastAPI documentation and community
- SQLAlchemy team
- Supabase for database hosting
