# Makefile for managing OPAL, application services, and frontend

# Define compose files
AUTHZ_COMPOSE_FILE=authZ/docker-compose.yml
BACKEND_COMPOSE_FILE=backend/docker-compose.yml
FRONTEND_COMPOSE_FILE=frontend/docker-compose.yml

# Define common commands
DOCKER_COMPOSE=docker compose
UP_CMD=up -d
DOWN_CMD=stop
BUILD_CMD=build
LOGS_CMD=logs -f
NETWORK_NAME=app_network

# Create the network (if it doesn't exist already)
create-network:
	@docker network inspect $(NETWORK_NAME) >/dev/null 2>&1 || \
		docker network create $(NETWORK_NAME)

# Start the authZ compose services (OPAL and dependencies)
start-authZ: create-network
	$(DOCKER_COMPOSE) -f $(AUTHZ_COMPOSE_FILE) $(UP_CMD)

# Stop the authZ compose services
stop-authZ:
	$(DOCKER_COMPOSE) -f $(AUTHZ_COMPOSE_FILE) $(DOWN_CMD)

# Restart the authZ compose services
restart-authZ: stop-authZ start-authZ

# Build the authZ compose services
build-authZ:
	$(DOCKER_COMPOSE) -f $(AUTHZ_COMPOSE_FILE) $(BUILD_CMD)

# View logs for authZ compose services
logs-authZ:
	$(DOCKER_COMPOSE) -f $(AUTHZ_COMPOSE_FILE) $(LOGS_CMD)

# Start the backend compose services
start-backend: create-network
	$(DOCKER_COMPOSE) -f $(BACKEND_COMPOSE_FILE) $(UP_CMD)

# Stop the backend compose services
stop-backend:
	$(DOCKER_COMPOSE) -f $(BACKEND_COMPOSE_FILE) $(DOWN_CMD)

# Restart the backend compose services
restart-backend: stop-backend start-backend

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

# Restart the frontend compose services
restart-frontend: stop-frontend start-frontend

# Build the frontend compose services
build-frontend:
	$(DOCKER_COMPOSE) -f $(FRONTEND_COMPOSE_FILE) $(BUILD_CMD)

# View logs for frontend compose services
logs-frontend:
	$(DOCKER_COMPOSE) -f $(FRONTEND_COMPOSE_FILE) $(LOGS_CMD)

# Stop all services
stop-all:
	@make stop-authZ
	@make stop-backend
	@make stop-frontend

# Restart all services
restart-all:
	@make restart-authZ
	@make restart-backend
	@make restart-frontend

# Start authZ, backend, and frontend services
start-all: create-network
	@make start-authZ
	@make start-backend
	@make start-frontend

# Build authZ, backend, and frontend services
build-all:
	@make build-authZ
	@make build-backend
	@make build-frontend

# View logs for all services
logs-all:
	@make logs-authZ
	@make logs-backend
	@make logs-frontend
