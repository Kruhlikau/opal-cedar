# Makefile for managing OPAL, application services, and frontend

# Define compose files
AUTH_COMPOSE_FILE=authZ/docker-compose.yml
BACKEND_COMPOSE_FILE=backend/docker-compose.yml
FRONTEND_COMPOSE_FILE=frontend/docker-compose.yml

# Define common commands
DOCKER_COMPOSE=docker compose
UP_CMD=up -d
DOWN_CMD=down
BUILD_CMD=build
LOGS_CMD=logs -f
NETWORK_NAME=app_network

# Create the network (if it doesn't exist already)
create-network:
	@docker network inspect $(NETWORK_NAME) >/dev/null 2>&1 || \
		docker network create $(NETWORK_NAME)

# Start the auth compose services (OPAL and dependencies)
start-auth: create-network
	$(DOCKER_COMPOSE) -f $(AUTH_COMPOSE_FILE) $(UP_CMD)

# Stop the auth compose services
stop-auth:
	$(DOCKER_COMPOSE) -f $(AUTH_COMPOSE_FILE) $(DOWN_CMD)

# Build the auth compose services
build-auth:
	$(DOCKER_COMPOSE) -f $(AUTH_COMPOSE_FILE) $(BUILD_CMD)

# View logs for auth compose services
logs-auth:
	$(DOCKER_COMPOSE) -f $(AUTH_COMPOSE_FILE) $(LOGS_CMD)

# Start the backend compose services
start-backend: create-network
	$(DOCKER_COMPOSE) -f $(BACKEND_COMPOSE_FILE) $(UP_CMD)

# Stop the backend compose services
stop-backend:
	$(DOCKER_COMPOSE) -f $(BACKEND_COMPOSE_FILE) $(DOWN_CMD)

# Build the backend compose services
build-backend:
	$(DOCKER_COMPOSE) -f $(BACKEND_COMPOSE_FILE) $(BUILD_CMD)

# View logs for backend compose services
logs-backend:
	$(DOCKER_COMPOSE) -f $(BACKEND_COMPOSE_FILE) $(LOGS_CMD)

# Start the frontend compose services
start-frontend: create-network
	$(DOCKER_COMPOSE) -f $(FRONTEND_COMPOSE_FILE) $(UP_CMD)

# Stop the frontend compose services
stop-frontend:
	$(DOCKER_COMPOSE) -f $(FRONTEND_COMPOSE_FILE) $(DOWN_CMD)

# Build the frontend compose services
build-frontend:
	$(DOCKER_COMPOSE) -f $(FRONTEND_COMPOSE_FILE) $(BUILD_CMD)

# View logs for frontend compose services
logs-frontend:
	$(DOCKER_COMPOSE) -f $(FRONTEND_COMPOSE_FILE) $(LOGS_CMD)

# Stop all services
stop-all:
	@make stop-auth
	@make stop-backend
	@make stop-frontend

# Start both auth, backend, and frontend services
start-all: create-network
	@make start-auth
	@make start-backend
	@make start-frontend

# Build both auth, backend, and frontend services
build-all:
	@make build-auth
	@make build-backend
	@make build-frontend

# View logs for all services
logs-all:
	@make logs-auth
	@make logs-backend
	@make logs-frontend
