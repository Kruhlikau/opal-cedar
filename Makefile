# Makefile for managing OPAL and application services

# Define compose files
AUTH_COMPOSE_FILE=docker-compose.yml
APP_COMPOSE_FILE=app/docker-compose.yml

# Define common commands
DOCKER_COMPOSE=docker compose
UP_CMD=up -d
DOWN_CMD=down
BUILD_CMD=build
LOGS_CMD=logs -f
NETWORK_NAME=app_network  # Define the network name

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

# Start the app compose services
start-app: create-network
	$(DOCKER_COMPOSE) -f $(APP_COMPOSE_FILE) $(UP_CMD)

# Stop the app compose services
stop-app:
	$(DOCKER_COMPOSE) -f $(APP_COMPOSE_FILE) $(DOWN_CMD)

# Build the app compose services
build-app:
	$(DOCKER_COMPOSE) -f $(APP_COMPOSE_FILE) $(BUILD_CMD)

# View logs for app compose services
logs-app:
	$(DOCKER_COMPOSE) -f $(APP_COMPOSE_FILE) $(LOGS_CMD)

# Stop all services
stop-all:
	@make stop-auth
	@make stop-app

# Start both auth and app services
start-all: create-network
	@make start-auth
	@make start-app

# Build both auth and app services
build-all:
	@make build-auth
	@make build-app

# View logs for all services
logs-all:
	@make logs-auth
	@make logs-app
