# 🧠 RAG Quiz Generation Backend

A Django-based AI backend system for **automated quiz generation using RAG (Retrieval-Augmented Generation)**.

Built with:

- Python
- Django
- Django REST Framework
- ChromaDB (Vector Database)
- Docker
- AI-powered quiz generation pipeline

---

## 📁 Project Structure
```bash

RAG-Quiz-Generation-Backend/
├── api/ # Core application logic
│ ├── books/ # Knowledge base (learning materials)
│ │ ├── Event Planning and Coordination.txt
│ │ ├── Marketing and Promotion in Event Management.txt
│ │ └── ...
│
│ ├── db/ # Vector databases (ChromaDB)
│ │ ├── chroma_db/
│ │ ├── chroma_db_web_crawl/
│ │ └── epa_chroma_db/
│
│ ├── views_folder/ # API endpoints (business logic layer)
│ │ ├── course_view.py
│ │ ├── login_view.py
│ │ ├── quiz_view.py
│ │ ├── school_view.py
│ │ ├── student_view.py
│ │ ├── teacher_view.py
│ │ ├── unit_view.py
│
│ ├── models.py # Database schema
│ ├── serializers.py # API serialization layer
│ ├── quiz_generator.py # Core RAG quiz generation engine
│ ├── utils.py # Helper functions
│ ├── urls.py # API routing
│ ├── admin.py
│ ├── views.py
│ └── apps.py
│
├── core/ # Django project configuration
│ ├── settings.py # Project settings
│ ├── urls.py # Root routing
│ ├── asgi.py
│ ├── wsgi.py
│
├── manage.py # Django CLI entry point
├── requirements.txt # Python dependencies
├── dockerfile # Container build config
├── docker-compose.yml # Multi-service orchestration
├── entrypoint.sh # Container startup script
└── README.md

```


---

## 🧠 System Overview

This backend powers an **AI-driven quiz generation system** using:

### 🔍 Retrieval-Augmented Generation (RAG)

- Stores educational content in `books/`
- Converts content into embeddings
- Stores embeddings in **ChromaDB**
- Retrieves relevant context during quiz generation
- Uses AI logic in `quiz_generator.py`

---

## ⚙️ Architecture Design

This system follows a **layered Django + AI pipeline architecture**:

### 1. Data Layer
- `books/` → Raw educational content
- `db/` → Vector storage (ChromaDB)

### 2. Application Layer
- `models.py` → Database schema
- `serializers.py` → Data transformation

### 3. Business Logic Layer
- `views_folder/` → API endpoints
- `quiz_generator.py` → AI quiz engine

### 4. Core Layer
- `core/` → Django project configuration

---

## 🚀 Key Features

- AI-powered quiz generation (RAG-based)
- Vector database integration (ChromaDB)
- Multi-role system (Students, Teachers, Schools)
- Dynamic course & unit management
- RESTful API architecture
- Scalable modular design

---

## 🔌 API Structure

Base API endpoints:
/api/



### Main endpoints:

- `/api/login/` → Authentication
- `/api/student/` → Student management
- `/api/teacher/` → Teacher management
- `/api/school/` → School management
- `/api/course/` → Course data
- `/api/unit/` → Learning units
- `/api/quiz/` → Quiz generation system

---

## 🧠 AI / RAG Engine

Core logic lives in:
api/quiz_generator.py


### Responsibilities:

- Embedding generation
- Context retrieval from ChromaDB
- Prompt engineering
- Quiz question generation
- Answer structuring

---

## 🗄️ Vector Database

Stored in:

api/db/


Includes:

- `chroma_db` → Main embeddings store
- `chroma_db_web_crawl` → Web-scraped knowledge base
- `epa_chroma_db` → Event planning dataset embeddings

---

## 🐳 Docker Deployment

### Build containers
```bash id="m2v7k1"
docker-compose up --build # to start container
docker-compose down  # to stop container
```

## ⚙️ Setup Instructions

### Create a virtual environment and activate it 

```bash
python -m venv venv

venv\Scripts\activate   # Windows
source venv/bin/activate  # Mac/Linux
```

###  Install Dependencies, Migrate and Run Server 

```bash
pip install -r requirements.txt

python manage.py migrate

python manage.py runserver
```

