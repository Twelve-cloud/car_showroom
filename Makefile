devstart: docker-compose-dev.yaml
	sudo docker compose --env-file=.env.dev -f docker-compose-dev.yaml up --force-recreate --build

devstop: docker-compose-dev.yaml
	sudo docker compose -f docker-compose-dev.yaml down

prodstart: docker-compose-prod.yaml
	sudo docker compose --env-file=.env.prod -f docker-compose-prod.yaml up --force-recreate --build

prodstop: docker-compose-prod.yaml
	sudo docker compose -f docker-compose-prod.yaml down

docs:
	cd car_salon_activities/docs && make html