create: docker-compose.yaml
	sudo docker compose up --force-recreate --build

delete: docker-compose.yaml
	sudo docker compose down

docs:
	cd car_salon_activities && cd docs && make html && sphinx-build -M coverage . coverage