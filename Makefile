include .env
export


# PROD

COMPOSE_PROD := \
	-f docker-compose.yaml \
	-f ${COMPOSE_PROD_DB} \
	-f ${COMPOSE_PROD_RABBIT} \
	-f ${COMPOSE_PROD_REDIS} \
	-f ${COMPOSE_PROD_WEB} \

COMPOSE_PROD_ENV := \
	--env-file=.env \
	--env-file=env/production/.env.prod.compose \

prodstart: docker-compose.yaml
	sudo docker compose -p prod ${COMPOSE_PROD_ENV} ${COMPOSE_PROD} up --build --force-recreate

prodstop: docker-compose.yaml
	sudo docker compose -p prod ${COMPOSE_PROD_ENV} ${COMPOSE_PROD} down


# DEV

COMPOSE_DEV := \
	-f docker-compose.yaml \
	-f ${COMPOSE_DEV_DB} \
	-f ${COMPOSE_DEV_RABBIT} \
	-f ${COMPOSE_DEV_REDIS} \
	-f ${COMPOSE_DEV_WEB} \

COMPOSE_DEV_ENV := \
	--env-file=.env \
	--env-file=env/development/.env.dev.compose \

devstart: docker-compose.yaml
	sudo docker compose -p dev ${COMPOSE_DEV_ENV} ${COMPOSE_DEV} up --build --force-recreate

devstop: docker-compose.yaml
	sudo docker compose -p dev ${COMPOSE_DEV_ENV} ${COMPOSE_DEV} down


# TESTS

COMPOSE_TESTS := \
	-f docker-compose.yaml \
	-f ${COMPOSE_TESTS_DB} \
	-f ${COMPOSE_TESTS_RABBIT} \
	-f ${COMPOSE_TESTS_REDIS} \
	-f ${COMPOSE_TESTS_WEB} \

COMPOSE_TESTS_ENV := \
	--env-file=.env \
	--env-file=env/tests/.env.tests.compose \

itests:
	./test.sh


# DOCS

docs:
	cd src/docs && make html