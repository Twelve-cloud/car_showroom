include .env
export


docs:
	cd car_salon_activities/docs && make html


COMPOSE_PROD := \
	-f docker-compose.yaml \
	-f ${COMPOSE_PROD_DB} \
	-f ${COMPOSE_PROD_RABBIT} \
	-f ${COMPOSE_PROD_REDIS} \
	-f ${COMPOSE_PROD_WEB} \

prodstart: docker-compose.yaml
	sudo docker compose ${COMPOSE_PROD} up --build --force-recreate

prodstop: docker-compose.yaml
	sudo docker compose ${COMPOSE_PROD} down


COMPOSE_DEV := \
	-f docker-compose.yaml \
	-f ${COMPOSE_DEV_DB} \
	-f ${COMPOSE_DEV_RABBIT} \
	-f ${COMPOSE_DEV_REDIS} \
	-f ${COMPOSE_DEV_WEB} \

devstart: docker-compose.yaml
	sudo docker compose ${COMPOSE_DEV} up --build --force-recreate

devstop: docker-compose.yaml
	sudo docker compose ${COMPOSE_DEV} down
