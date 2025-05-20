WEB_DB_NAME = odoo_development
DOCKER = docker
DOCKER_COMPOSE = $(DOCKER) compose
CONTAINER_ODOO = odoo
CONTAINER_DB = odoo_development-odoo-postgres-1

help:
	@echo "Available targets:"
	@echo "  start        		- Start Odoo and DB containers"
	@echo "  stop         		- Stop and remove containers"
	@echo "  restart      		- Restart containers"
	@echo "  console      		- Enter Odoo container shell"
	@echo "  psql         		- Enter Postgres psql prompt"
	@echo "  logs-odoo    		- View Odoo logs"
	@echo "  logs-db      		- View Postgres logs"
	@echo "  addon <addon_name> - Restart Instance and Upgrade Addons"

start:
	$(DOCKER) compose up -d

stop:
	$(DOCKER) compose down

restart:
	$(DOCKER) compose restart

console:
	$(DOCKER) exec -it $(CONTAINER_ODOO) odoo shell --db_host=$(CONTAINER_DB) -d $(WEB_DB_NAME) -r $(CONTAINER_ODOO) -w $(CONTAINER_ODOO)

psql:
	$(DOCKER) exec -it $(CONTAINER_DB) psql -U $(CONTAINER_ODOO) -d $(WEB_DB_NAME)

define log_target
	@if [ "$(1)" = "odoo" ]; then \
		$(DOCKER_COMPOSE) logs -f $(CONTAINER_ODOO); \
	elif [ "$(1)" = "db" ]; then \
		$(DOCKER_COMPOSE) logs -f $(CONTAINER_DB); \
	else \
		echo "Invalid Logs Target. Use 'make logs odoo' or 'make logs db'"; \
	fi
endef

logs:
	$(call log_target,$(word 2, $(MAKECMDGOALS)))

define upgrade_addon
	$(DOCKER) exec -it $(CONTAINER_ODOO) odoo --db_host=$(CONTAINER_DB) \
	-d $(WEB_DB_NAME) -r $(CONTAINER_ODOO) -w $(CONTAINER_ODOO) -u $(1)
endef

addon:restart
	$(call upgrade_addon,$(word 2,$(MAKECMDGOALS)))


.PHONY : start stop restart console psql logs odoo db addon