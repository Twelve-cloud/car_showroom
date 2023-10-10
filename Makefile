create: docker-compose.yaml
	sudo docker compose up --force-recreate --build

delete: docker-compose.yaml
	sudo docker compose down
