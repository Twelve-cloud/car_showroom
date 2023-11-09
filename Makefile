include .env
export


COMPOSE_PROD := \
	-f docker-compose.yaml \
	-f ${COMPOSE_PROD_DB} \
	-f ${COMPOSE_PROD_RABBIT} \
	-f ${COMPOSE_PROD_REDIS} \
	-f ${COMPOSE_PROD_WEB} \

COMPOSE_PROD_ENV := \
	--env-file=.env \
	--env-file=env/production/.env.prod.django \
	--env-file=env/production/.env.prod.postgres \
	--env-file=env/production/.env.prod.rabbitmq \
	--env-file=env/production/.env.prod.redis \

prodstart: docker-compose.yaml
	sudo docker compose ${COMPOSE_PROD_ENV} ${COMPOSE_PROD} up --build --force-recreate

prodstop: docker-compose.yaml
	sudo docker compose ${COMPOSE_PROD_ENV} ${COMPOSE_PROD} down


COMPOSE_DEV := \
	-f docker-compose.yaml \
	-f ${COMPOSE_DEV_DB} \
	-f ${COMPOSE_DEV_RABBIT} \
	-f ${COMPOSE_DEV_REDIS} \
	-f ${COMPOSE_DEV_WEB} \

COMPOSE_DEV_ENV := \
	--env-file=.env \
	--env-file=env/development/.env.dev.django \
	--env-file=env/development/.env.dev.postgres \
	--env-file=env/development/.env.dev.rabbitmq \
	--env-file=env/development/.env.dev.redis \

devstart: docker-compose.yaml
	sudo docker compose ${COMPOSE_DEV_ENV} ${COMPOSE_DEV} up --build --force-recreate

devstop: docker-compose.yaml
	sudo docker compose ${COMPOSE_DEV_ENV} ${COMPOSE_DEV} down


COMPOSE_TESTS := \
	-f docker-compose.yaml \
	-f ${COMPOSE_TESTS_DB} \
	-f ${COMPOSE_TESTS_RABBIT} \
	-f ${COMPOSE_TESTS_REDIS} \
	-f ${COMPOSE_TESTS_WEB} \

COMPOSE_TESTS_ENV := \
	--env-file=.env \
	--env-file=env/tests/.env.tests.django \
	--env-file=env/tests/.env.tests.postgres \
	--env-file=env/tests/.env.tests.rabbitmq \
	--env-file=env/tests/.env.tests.redis \

tests:
	./test.sh


docs:
	cd car_salon_activities/docs && make html