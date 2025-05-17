# Django Notes-Taking API

This repository provides a backend for a notes-taking application. It uses Django and Django REST Framework, with JWT authentication (`djangorestframework-simplejwt`) and a MySQL database, all running in Docker containers.

## Requirements

- Docker & Docker Compose installed locally.
- Python and MySQL installed if running outside Docker (not required when using Docker).

## Installation

1. **Clone the repository**
2. **Configure environment variables**: Create a `.env` file or ensure the following are set in your environment:


# MYSQL_DATABASE=notetaking_db
# MYSQL_USER=django_user
# MYSQL_PASSWORD=Inpl2010@1

These values are loaded by `settings.py`:contentReference[oaicite:10]{index=10}. In the provided `docker-compose.yml`, defaults are given for convenience.
3. **Build and run with Docker Compose**:
```bash
docker-compose up --build
