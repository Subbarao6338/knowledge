# Docker Cheatsheet

## Images

```bash
docker images                        # list local images
docker pull ubuntu:24.04
docker build -t myapp:latest .
docker build -t myapp:latest -f Dockerfile.prod .
docker build --no-cache -t myapp:latest .
docker build --build-arg VERSION=1.2 -t myapp:latest .

docker tag myapp:latest myrepo/myapp:v1.0
docker push myrepo/myapp:v1.0
docker rmi myapp:latest
docker rmi $(docker images -q)             # remove all images
docker image prune                            # remove dangling images
docker image prune -a                            # remove all unused images
docker history myapp:latest                         # show image layer history
docker inspect myapp:latest
docker save myapp:latest -o myapp.tar             # export image to a tarball
docker load -i myapp.tar                             # import image from tarball
```

## Containers

```bash
docker run ubuntu:24.04 echo "hello"
docker run -it ubuntu:24.04 bash                  # interactive shell
docker run -d --name myapp myapp:latest              # detached (background)
docker run -d -p 8080:80 myapp:latest                   # port mapping (host:container)
docker run -d -v /host/path:/container/path myapp:latest    # bind mount
docker run -d -v myvolume:/data myapp:latest                   # named volume
docker run -e KEY=value -e KEY2=value2 myapp:latest               # env vars
docker run --env-file .env myapp:latest
docker run --rm myapp:latest                                 # auto-remove after exit
docker run --restart unless-stopped myapp:latest                # restart policy
docker run --memory 512m --cpus 1.5 myapp:latest                   # resource limits
docker run --network mynetwork myapp:latest

docker ps                       # running containers
docker ps -a                       # all containers (incl. stopped)
docker ps -q                          # just container IDs

docker start mycontainer
docker stop mycontainer
docker restart mycontainer
docker pause mycontainer
docker unpause mycontainer
docker kill mycontainer                  # force stop (SIGKILL)
docker rm mycontainer
docker rm -f mycontainer                    # force remove running container
docker rm $(docker ps -aq)                     # remove all containers
docker container prune                            # remove all stopped containers

docker exec -it mycontainer bash            # shell into a running container
docker exec mycontainer ls /app
docker logs mycontainer
docker logs -f mycontainer                     # follow logs live
docker logs --tail 100 mycontainer
docker logs --since 10m mycontainer

docker inspect mycontainer                # full metadata as JSON
docker inspect -f '{{.NetworkSettings.IPAddress}}' mycontainer
docker top mycontainer                       # processes running inside the container
docker stats                                    # live resource usage for all containers
docker stats mycontainer

docker cp file.txt mycontainer:/app/                # host -> container
docker cp mycontainer:/app/file.txt .                   # container -> host

docker diff mycontainer                # filesystem changes since start
docker commit mycontainer myimage:snapshot   # save a running container's state as an image
docker rename oldname newname
docker port mycontainer                          # show port mappings
docker attach mycontainer                            # attach to a running container's stdout/stdin
```

## Dockerfile Essentials

```dockerfile
FROM python:3.12-slim AS base

# Metadata / env
LABEL maintainer="you@example.com"
ENV PYTHONUNBUFFERED=1
ARG BUILD_ENV=production

WORKDIR /app

# Dependency layer cached separately from code (speeds up rebuilds)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Non-root user (security best practice)
RUN useradd -m appuser
USER appuser

EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s CMD curl -f http://localhost:8080/health || exit 1

ENTRYPOINT ["python"]
CMD ["app.py"]                    # default args to ENTRYPOINT, overridable at `docker run`

# Multi-stage build — keeps final image small
FROM node:20 AS builder
WORKDIR /app
COPY . .
RUN npm install && npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
```

**Key Dockerfile instructions:**

| Instruction | Purpose |
|---|---|
| `FROM` | Base image |
| `RUN` | Execute a command during build (creates a layer) |
| `COPY` / `ADD` | Copy files into the image (`ADD` also handles URLs/tar extraction — prefer `COPY` otherwise) |
| `WORKDIR` | Set working directory for subsequent instructions |
| `ENV` | Set environment variable (persists at runtime) |
| `ARG` | Build-time-only variable |
| `EXPOSE` | Document the port the container listens on (doesn't actually publish it) |
| `USER` | Set the user to run subsequent instructions / the container process |
| `ENTRYPOINT` | Fixed command that always runs |
| `CMD` | Default arguments (overridable) |
| `VOLUME` | Declare a mount point |
| `HEALTHCHECK` | Define how Docker checks container health |

## docker-compose

```yaml
# docker-compose.yml
version: "3.9"

services:
  web:
    build: .
    ports:
      - "8080:80"
    environment:
      - DEBUG=true
    env_file:
      - .env
    volumes:
      - ./app:/app
      - data:/data
    depends_on:
      - db
    restart: unless-stopped
    networks:
      - mynetwork

  db:
    image: postgres:16
    environment:
      POSTGRES_PASSWORD: secret
    volumes:
      - dbdata:/var/lib/postgresql/data
    networks:
      - mynetwork

volumes:
  data:
  dbdata:

networks:
  mynetwork:
```

```bash
docker compose up                    # start all services (foreground)
docker compose up -d                    # detached
docker compose up --build                  # rebuild images before starting
docker compose down                           # stop and remove containers/networks
docker compose down -v                           # also remove named volumes
docker compose ps
docker compose logs -f
docker compose logs -f web                    # logs for one service
docker compose exec web bash                     # shell into a running service
docker compose build
docker compose restart web
docker compose stop; docker compose start
docker compose config                              # validate and view resolved config
docker compose pull                                   # pull latest images for all services
```

## Volumes & Networks

```bash
docker volume ls
docker volume create myvolume
docker volume inspect myvolume
docker volume rm myvolume
docker volume prune

docker network ls
docker network create mynetwork
docker network create --driver bridge mynetwork
docker network inspect mynetwork
docker network connect mynetwork mycontainer
docker network disconnect mynetwork mycontainer
docker network rm mynetwork
docker network prune
```

## Registry & Auth

```bash
docker login
docker login myregistry.com
docker logout

docker pull myregistry.com/myimage:tag
docker push myregistry.com/myimage:tag

# Cloud-specific auth helpers (also see AWS/Azure/GCP cheatsheets)
aws ecr get-login-password | docker login --username AWS --password-stdin <account>.dkr.ecr.<region>.amazonaws.com
gcloud auth configure-docker europe-west3-docker.pkg.dev
az acr login --name myacr
```

## Cleanup & System

```bash
docker system df               # disk usage summary
docker system prune                # remove unused containers, networks, dangling images
docker system prune -a                # also remove unused images (not just dangling)
docker system prune -a --volumes         # also remove unused volumes (careful!)

docker info                    # daemon-level info
docker version                    # client + server version
```

## Common Patterns

```bash
# Run a one-off command and clean up automatically
docker run --rm -v $(pwd):/app -w /app python:3.12 python script.py

# Interactive debugging shell inside a running container
docker exec -it $(docker ps -qf "name=myapp") bash

# Copy build output out of a container without running it
docker create --name temp myimage
docker cp temp:/app/dist ./dist
docker rm temp

# View environment variables inside a running container
docker exec mycontainer env

# Limit container to specific CPUs
docker run --cpuset-cpus="0,1" myimage

# Health check status
docker inspect --format='{{json .State.Health}}' mycontainer
```

## Common Gotchas

- Each `RUN`/`COPY`/`ADD` creates a new layer — order Dockerfile instructions so rarely-changing steps (installing dependencies) come before frequently-changing ones (copying source code), to maximize build cache reuse.
- `ENTRYPOINT` + `CMD` together: `CMD` args are passed to `ENTRYPOINT` and can be overridden at `docker run`, but `ENTRYPOINT` itself requires `--entrypoint` to override.
- Bind mounts (`-v /host:/container`) reflect host filesystem permissions/UID — can cause permission errors inside containers running as non-root.
- `docker rm -f` on a container doesn't remove its volumes unless you also pass `-v`.
- Images accumulate — dangling/unused images and stopped containers silently consume disk; run `docker system prune` periodically.
- `EXPOSE` in a Dockerfile is documentation only — it does not actually publish the port; you still need `-p` at `docker run` (or `ports:` in compose).
