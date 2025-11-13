# 🐳 Docker Implementation Guide

Complete guide for running the Gemini API project with Docker and Docker Compose.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick Start](#quick-start)
3. [Project Structure](#project-structure)
4. [Services Overview](#services-overview)
5. [Configuration](#configuration)
6. [Building and Running](#building-and-running)
7. [Accessing Services](#accessing-services)
8. [Useful Commands](#useful-commands)
9. [Troubleshooting](#troubleshooting)
10. [Production Deployment](#production-deployment)

---

## Prerequisites

### Required Software

- **Docker**: Version 20.10 or higher
  - [Install Docker](https://docs.docker.com/get-docker/)
  
- **Docker Compose**: Version 1.29 or higher
  - Usually included with Docker Desktop

### Verify Installation

```bash
docker --version
docker-compose --version
```

Expected output:
```
Docker version 24.0.0 (or higher)
Docker Compose version 2.20.0 (or higher)
```

### System Requirements

- **RAM**: Minimum 2GB (4GB recommended)
- **Disk Space**: 3GB for Docker images + database
- **CPU**: Dual-core or better

---

## Quick Start

### 1. Clone or Setup the Project

```bash
cd e:\Alexis\python\gemini api
```

### 2. Create Environment File

```bash
copy .env.example .env
```

Or on PowerShell:
```powershell
Copy-Item .env.example .env
```

**⚠️ Important**: Update the `.env` file with your own values:
- `SECRET_KEY`: Generate a random key
- Database password
- CORS origins for your domain

### 3. Build Docker Images

```bash
docker-compose build
```

This will create 4 images:
- `gemini-api:latest` (FastAPI application)
- `postgres:15-alpine` (Database)
- `nginx:latest` (Frontend server)
- `dpage/pgadmin4:latest` (Database management)

### 4. Start All Services

```bash
docker-compose up -d
```

**Output:**
```
✓ Network fastapi_network Created
✓ Volume postgres_data Created
✓ Volume pgadmin_data Created
✓ Service db started
✓ Service api started
✓ Service frontend started
✓ Service pgadmin started
```

### 5. Verify Services Are Running

```bash
docker-compose ps
```

Expected output (all showing "healthy" or "running"):
```
NAME                COMMAND                   SERVICE      STATUS
db                  "docker-entrypoint..."    db           healthy
api                 "uvicorn main:app..."     api          healthy
frontend            "nginx -g 'daemon off'"   frontend     running
pgadmin             "/entrypoint.sh"          pgadmin      running
```

### 6. Access the Application

- **Frontend**: http://localhost
- **API Swagger**: http://localhost/docs
- **API ReDoc**: http://localhost/redoc
- **pgAdmin**: http://localhost:5050

---

## Project Structure

```
gemini api/
├── Dockerfile                 # Multi-stage build for API
├── docker-compose.yml         # Service orchestration (4 services)
├── .dockerignore             # Excludes unnecessary files from image
├── nginx.conf                # Nginx configuration for frontend
├── init.sql                  # PostgreSQL initialization script
├── .env.example              # Environment variables template
│
├── main.py                   # FastAPI application (8 endpoints)
├── auth.py                   # JWT token generation & validation
├── models.py                 # SQLAlchemy database models
├── schemas.py                # Pydantic request/response models
├── crud.py                   # Database CRUD operations
├── database.py               # SQLAlchemy async configuration
├── logging_config.py         # Custom logging setup
├── conftest.py               # pytest configuration
│
├── frontend/                 # Web UI (HTML/CSS/JS)
│   ├── index.html           # Main interface
│   ├── main.js              # API consumer logic
│   └── styles.css           # Modern responsive styling
│
├── logs/                     # Application logs (created at runtime)
├── requirements.txt          # Python dependencies
└── test_main.py             # 17 test cases (100% passing)
```

---

## Services Overview

### 1. PostgreSQL (db)

**Image**: `postgres:15-alpine`

**Responsibilities**:
- Data persistence for users, tokens, logs
- Full ACID compliance
- Automatic health checks

**Connection Details**:
```
Host: db
Port: 5432
Database: gemini_api
Username: admin
Password: (from .env DATABASE_URL)
```

**Volumes**:
- `postgres_data:/var/lib/postgresql/data` - Persistent database files
- `./init.sql:/docker-entrypoint-initdb.d/init.sql` - Auto-run initialization

**Health Check**: 
```
pg_isready -U admin -d gemini_api
```

### 2. FastAPI (api)

**Image**: `gemini-api:latest` (built from Dockerfile)

**Responsibilities**:
- Handle all API requests
- JWT authentication
- Rate limiting
- Request logging

**Configuration**:
```
Host: 0.0.0.0
Port: 8000
Workers: Auto-calculated based on CPU cores
```

**Volumes**:
- `./logs:/app/logs` - Application logs on host machine

**Environment Variables**:
- All from `.env` file
- Database connection
- JWT secrets
- API configuration

**Health Check**:
```
GET http://localhost:8000/health
```

**Exposed Endpoints**:
- `POST /api/register` - User registration
- `POST /api/token` - Login (get tokens)
- `POST /api/refresh` - Refresh access token
- `GET /api/users/me` - Get current user info
- `GET /api/users` - List all users
- `PUT /api/users/{user_id}` - Update user
- `DELETE /api/users/{user_id}` - Delete user
- `GET /health` - Health check

### 3. Nginx (frontend)

**Image**: `nginx:latest`

**Responsibilities**:
- Serve static frontend files (HTML/CSS/JS)
- Proxy API requests to FastAPI service
- Gzip compression for static assets
- Rate limiting for frontend requests
- Cache control for static files

**Configuration** (`nginx.conf`):
- Root directory: `/usr/share/nginx/html`
- Static files cache: 30 days
- Gzip compression enabled
- Rate limiting: 10 req/s (general), 30 req/s (API)

**Volume**:
- `./frontend:/usr/share/nginx/html:ro` - Frontend files (read-only)

**Port**: 80 (HTTP)

**Routes**:
- `/` - Serve index.html (SPA routing)
- `/api/*` - Proxy to FastAPI
- `/docs` - Proxy Swagger UI
- `/redoc` - Proxy ReDoc
- `/health` - Health check
- `/openapi.json` - OpenAPI schema

### 4. pgAdmin (pgadmin)

**Image**: `dpage/pgadmin4:latest`

**Responsibilities**:
- Web-based PostgreSQL management
- Visual database administration
- Query editor
- Database backup/restore

**Access**:
- URL: http://localhost:5050
- Default Email: admin@example.com (change in .env)
- Default Password: admin123 (change in .env)

**Volume**:
- `pgadmin_data:/var/lib/pgadmin` - Persistent configuration

**⚠️ Important**: Change default credentials in production!

---

## Configuration

### Environment Variables

All configuration is in `.env` file. Key variables:

**Database**:
```
DATABASE_URL=postgresql+asyncpg://admin:password@db:5432/gemini_api
DATABASE_POOL_SIZE=20
```

**JWT**:
```
SECRET_KEY=your-32-character-random-string
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

**API**:
```
HOST=0.0.0.0
PORT=8000
ENVIRONMENT=production
```

**CORS** (comma-separated):
```
CORS_ORIGINS=http://localhost,http://localhost:80
```

**Rate Limiting**:
```
RATE_LIMIT_REGISTER=5/minute
RATE_LIMIT_LOGIN=10/minute
RATE_LIMIT_REFRESH=20/minute
```

### Generate Secure SECRET_KEY

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Example output:
```
Drmhze6EPcv0fN_81Bj-nA_7xU1PXkr6DQeXHKl5Pl8
```

Copy this into `.env`:
```
SECRET_KEY=Drmhze6EPcv0fN_81Bj-nA_7xU1PXkr6DQeXHKl5Pl8
```

### Network Configuration

All services communicate via `fastapi_network` (Docker bridge network):

```
frontend (nginx) → api (FastAPI) → db (PostgreSQL)
                     ↓
                  logging
```

No need to expose internal ports between services. Only Nginx (port 80) is exposed to host.

---

## Building and Running

### Build Images

```bash
docker-compose build
```

**Optional: Build specific service**:
```bash
docker-compose build api
```

### Start Services

**Detached mode** (recommended):
```bash
docker-compose up -d
```

**Foreground mode** (see logs in real-time):
```bash
docker-compose up
```

**Start specific service**:
```bash
docker-compose up -d api
```

### Stop Services

```bash
docker-compose down
```

**Keep volumes** (preserve database):
```bash
docker-compose down
```

**Remove everything** (delete database):
```bash
docker-compose down -v
```

### View Logs

**All services**:
```bash
docker-compose logs -f
```

**Specific service**:
```bash
docker-compose logs -f api
docker-compose logs -f db
docker-compose logs -f frontend
```

**Last 50 lines**:
```bash
docker-compose logs -f --tail=50 api
```

### Restart Services

```bash
docker-compose restart
```

**Specific service**:
```bash
docker-compose restart api
```

---

## Accessing Services

### Frontend (Web UI)

**URL**: http://localhost

**Features**:
- User registration
- User login
- Token management
- API endpoint testing
- Real-time token expiry countdown

### API Documentation

**Swagger UI**: http://localhost/docs
**ReDoc**: http://localhost/redoc

**Manual API Testing**:
```bash
# Register
curl -X POST http://localhost/api/register \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"testuser\",\"email\":\"test@example.com\",\"password\":\"Test123!\"}"

# Login
curl -X POST http://localhost/api/token \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"testuser\",\"password\":\"Test123!\"}"

# Get current user (requires token)
curl -X GET http://localhost/api/users/me \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Database Management (pgAdmin)

**URL**: http://localhost:5050

**Steps**:
1. Login with credentials from `.env` (default: admin@example.com / admin123)
2. Add new server:
   - Name: gemini_api
   - Host: db
   - Port: 5432
   - Database: gemini_api
   - Username: admin
   - Password: (from .env)
3. View/edit data via web interface

### Direct Database Access

```bash
docker-compose exec db psql -U admin -d gemini_api
```

Then run SQL:
```sql
SELECT * FROM users;
SELECT * FROM users LIMIT 5;
\dt  -- List all tables
\d users  -- Describe users table
```

---

## Useful Commands

### Container Management

```bash
# View container status
docker-compose ps

# View resource usage
docker stats

# Inspect container configuration
docker-compose config

# Validate docker-compose.yml
docker-compose config --quiet

# Execute command in container
docker-compose exec api python -c "import main; print('API module OK')"

# View container IP addresses
docker-compose exec api ip addr show
```

### Logs and Debugging

```bash
# Tail logs (follow mode)
docker-compose logs -f api

# View logs with timestamps
docker-compose logs -t api

# View only errors
docker-compose logs api | grep -i error

# Save logs to file
docker-compose logs api > api_logs.txt

# Clear logs (if stored as files)
docker system prune --volumes
```

### Database Operations

```bash
# Backup database
docker-compose exec -T db pg_dump -U admin gemini_api > backup.sql

# Restore from backup
docker-compose exec -T db psql -U admin gemini_api < backup.sql

# Run SQL command
docker-compose exec db psql -U admin gemini_api -c "SELECT COUNT(*) FROM users;"
```

### Image Management

```bash
# List all images
docker images

# Remove unused images
docker image prune

# Remove specific image
docker rmi gemini-api:latest

# Rebuild without cache
docker-compose build --no-cache
```

### Network Diagnostics

```bash
# Test connectivity between containers
docker-compose exec api ping db

# Check DNS resolution
docker-compose exec api nslookup db

# View network details
docker network inspect fastapi_network

# Test API from inside container
docker-compose exec frontend curl http://api:8000/health
```

### Cleaning Up

```bash
# Stop all services, remove containers (keep volumes)
docker-compose down

# Remove everything including volumes
docker-compose down -v

# Remove unused Docker resources
docker system prune

# Deep clean (removes all unused images, containers, networks)
docker system prune -a
```

---

## Troubleshooting

### Service Won't Start

**Check logs**:
```bash
docker-compose logs -f api
docker-compose logs -f db
```

**Common issues**:

1. **Port already in use**
   ```bash
   # Find process using port 80
   netstat -ano | findstr :80
   # Kill process
   taskkill /PID <PID> /F
   ```

2. **Out of disk space**
   ```bash
   docker system prune -a
   docker system prune --volumes
   ```

3. **Permission denied**
   - Ensure Docker daemon is running
   - Add user to docker group (Linux): `sudo usermod -aG docker $USER`

### Database Connection Error

```
ERROR: could not connect to server: Connection refused
```

**Solution**:
```bash
# Wait for database to be ready
docker-compose exec db pg_isready -U admin

# Check if database exists
docker-compose exec db psql -U admin -l
```

### API Returns 502 Bad Gateway

**Issue**: Nginx can't reach FastAPI

**Solution**:
```bash
# Check if API service is healthy
docker-compose ps api

# Check API logs
docker-compose logs api

# Test connection from Nginx
docker-compose exec frontend curl http://api:8000/health
```

### Frontend Shows API Unreachable

**Issue**: JavaScript can't call API from browser

**Possible causes**:
1. CORS not configured correctly in `.env`
2. API service not running
3. Nginx not proxying correctly

**Solution**:
```bash
# Check CORS configuration
docker-compose exec api env | grep CORS

# Check Nginx logs
docker-compose logs frontend

# Verify API is responding
curl http://localhost/api/health

# Check Nginx config syntax
docker-compose exec frontend nginx -t
```

### High Memory Usage

**Symptoms**: Docker using excessive RAM

**Solution**:
```bash
# Limit service memory in docker-compose.yml:
services:
  api:
    deploy:
      resources:
        limits:
          memory: 512M
        reservations:
          memory: 256M
```

Then restart:
```bash
docker-compose up -d
```

### Database Disk Full

**Solution**:
```bash
# Remove old logs
docker-compose exec db rm -f /var/log/postgresql/*

# Vacuum database
docker-compose exec db psql -U admin gemini_api -c "VACUUM;"

# Check disk usage
docker-compose exec db du -sh /var/lib/postgresql/data
```

### Reset Everything

```bash
# Stop and remove all (including data)
docker-compose down -v

# Remove images
docker-compose rm -f

# Rebuild
docker-compose build --no-cache

# Start fresh
docker-compose up -d
```

---

## Production Deployment

### Pre-Deployment Checklist

- [ ] Change `ENVIRONMENT=production` in `.env`
- [ ] Generate new `SECRET_KEY` (see Configuration section)
- [ ] Update database password (strong, 16+ characters)
- [ ] Change pgAdmin credentials
- [ ] Update `CORS_ORIGINS` to your domain
- [ ] Set `RELOAD=false` in `.env`
- [ ] Review `nginx.conf` for your domain
- [ ] Enable HTTPS (modify nginx.conf)
- [ ] Set resource limits for containers
- [ ] Configure backup strategy

### Example Production Configuration

```bash
# .env (production)
ENVIRONMENT=production
SECRET_KEY=YOUR_SECURE_RANDOM_KEY_HERE
DATABASE_URL=postgresql+asyncpg://admin:YOUR_STRONG_PASSWORD@db:5432/gemini_api
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
API_TITLE=Gemini API Production
LOG_LEVEL=WARNING
```

### Enable HTTPS

Add to `nginx.conf`:

```nginx
server {
    listen 443 ssl http2;
    ssl_certificate /etc/nginx/certs/cert.pem;
    ssl_certificate_key /etc/nginx/certs/key.pem;
    
    # Redirect HTTP to HTTPS
}

server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}
```

### Database Backups

```bash
# Automatic daily backup script
# backup.sh
#!/bin/bash
BACKUP_DIR="/backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
docker-compose exec -T db pg_dump -U admin gemini_api > "$BACKUP_DIR/backup_$TIMESTAMP.sql"
gzip "$BACKUP_DIR/backup_$TIMESTAMP.sql"
```

### Monitoring and Logging

```bash
# Setup ELK Stack (Elasticsearch, Logstash, Kibana) for production logging
# Or use cloud logging service (AWS CloudWatch, Azure Monitor, etc.)

# Basic health check endpoint:
# GET http://yourdomain.com/health
# Response: {"status": "ok"}
```

### Scaling

For multiple API instances:

```yaml
services:
  api:
    deploy:
      replicas: 3
```

Then add load balancer (Nginx upstream):

```nginx
upstream api_backend {
    server api:8000;
    server api:8001;
    server api:8002;
}
```

### Security Recommendations

1. **Network Security**
   - Run Docker daemon on private network only
   - Use firewall to restrict access to container ports
   - Only expose port 80/443 publicly

2. **Image Security**
   - Run containers as non-root user (already configured)
   - Use specific image versions (not `latest`)
   - Scan images for vulnerabilities: `docker scan gemini-api`

3. **Secret Management**
   - Use Docker Secrets or HashiCorp Vault for production
   - Never commit `.env` with real passwords
   - Rotate secrets regularly

4. **Database Security**
   - Use strong passwords (20+ characters)
   - Enable PostgreSQL SSL connections
   - Restrict database access to API only
   - Regular backups to secure location

5. **API Security**
   - Keep dependencies updated: `pip list --outdated`
   - Enable rate limiting (already configured)
   - Use HTTPS only in production
   - Implement request validation

---

## Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [FastAPI Docker Deployment](https://fastapi.tiangolo.com/deployment/docker/)
- [PostgreSQL Docker Documentation](https://hub.docker.com/_/postgres)
- [Nginx Docker Documentation](https://hub.docker.com/_/nginx)

## Support

For issues or questions:

1. Check logs: `docker-compose logs -f`
2. Review this guide's Troubleshooting section
3. Verify configuration in `.env` file
4. Check Docker and Docker Compose versions
5. Ensure adequate system resources

---

**Last Updated**: 2024
**Version**: 1.0.0
**Status**: Production Ready ✅
