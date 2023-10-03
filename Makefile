create: docker-compose.yaml
	sudo docker-compose --env-file ./car_salon_activities/.env build
	sudo docker-compose --env-file ./car_salon_activities/.env up