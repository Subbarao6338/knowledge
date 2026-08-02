---
layout: default
title: "Docker Compose Cheatsheet"
---

# Docker Compose Cheatsheet

Docker Compose is a tool for defining and running multi-container Docker applications. With Compose, you use a YAML file to configure your application’s services, networks, and volumes.

---

## 1. Specification & Schema Structures

Modern Docker Compose uses the standardized Compose Specification (usually skipping the `version` key or keeping it at `3.8+`).

```yaml
services:
  web:
    image: nginx:alpine
    ports:
      - "80:80"
    networks:
      - app-tier
    volumes:
      - web-content:/usr/share/nginx/html
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '0.50'
          memory: 512M

networks:
  app-tier:
    driver: bridge

volumes:
  web-content:
```

---

## 2. Advanced Multi-Container Management

Configure service health checks, dependencies, and graceful startup behavior using `depends_on`.

```yaml
services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: app_db
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
    secrets:
      - db_password
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres -d app_db"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 15s

  backend:
    image: node:20-alpine
    depends_on:
      db:
        condition: service_healthy
    environment:
      DATABASE_URL: postgres://postgres:password@db:5432/app_db
    ports:
      - "3000:3000"

secrets:
  db_password:
    file: ./secrets/db_password.txt
```

---

## 3. Docker Compose CLI Commands

```bash
# Start all services defined in docker-compose.yml in background
docker compose up -d

# Start services using a different config file or multiple files (merging them)
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Stop running containers, removing networks, volumes, and custom images
docker compose down --volumes --rmi all

# View real-time log aggregates for all services with timestamps
docker compose logs -f --timestamps

# Rebuild images and launch services immediately
docker compose up -d --build

# Run a one-off command in a service container (automatically spins down container after run)
docker compose run --rm backend npm run migrate

# Inspect running container processes inside the stack
docker compose ps

# Check config verification and render merged settings
docker compose config
```

---

## 4. Multi-Stage Merging & Profiles

Using **Profiles** allows you to selectively run optional services (such as debuggers, test runners, or admin dashboards) only when explicitly called.

```yaml
services:
  app:
    image: python:3.11-slim
    command: uvicorn main:app --host 0.0.0.0

  pgadmin:
    image: dpage/pgadmin4
    profiles:
      - debug
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@app.com
      PGADMIN_DEFAULT_PASSWORD: admin
```

To run with profiles:
```bash
# Starts app only
docker compose up -d

# Starts app AND pgadmin
docker compose --profile debug up -d
```
