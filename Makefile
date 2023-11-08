devstart: docker-compose-dev.yaml
	sudo \
	docker compose \
	--env-file=./env/development/.env.dev.django \
	--env-file=./env/development/.env.dev.postgres \
	--env-file=./env/development/.env.dev.rabbitmq \
	--env-file=./env/development/.env.dev.redis \
	-f docker-compose-dev.yaml \
	up \
	--force-recreate \
	--build \

devstop: docker-compose-dev.yaml
	sudo \
	docker compose \
	--env-file=./env/development/.env.dev.django \
	--env-file=./env/development/.env.dev.postgres \
	--env-file=./env/development/.env.dev.rabbitmq \
	--env-file=./env/development/.env.dev.redis \
	-f docker-compose-dev.yaml \
	down \

prodstart: docker-compose-prod.yaml
	sudo \
	docker compose \
	--env-file=./env/production/.env.prod.django \
	--env-file=./env/production/.env.prod.postgres \
	--env-file=./env/production/.env.prod.rabbitmq \
	--env-file=./env/production/.env.prod.redis \
	-f docker-compose-prod.yaml \
	up \
	--force-recreate \
	--build \

prodstop: docker-compose-prod.yaml
	sudo \
	docker compose \
	--env-file=./env/production/.env.prod.django \
	--env-file=./env/production/.env.prod.postgres \
	--env-file=./env/production/.env.prod.rabbitmq \
	--env-file=./env/production/.env.prod.redis \
	-f docker-compose-prod.yaml \
	down \

docs:
	cd car_salon_activities/docs && make html