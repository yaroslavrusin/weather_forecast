init: docker_compose_run migrate_docker create_superuser_docker load_data_docker
start: docker_compose_run
stop: docker_compose_stop
rm: docker_compose_stop docker_rm_volumes docker_rm_images

# =================================================================================

migrate_docker:
	docker exec -it webserver python manage.py migrate
create_superuser_docker:
	docker exec -it webserver python manage.py createsuperuser --noinput
load_data_docker:
	docker exec -it webserver python manage.py loaddata ../city.json
docker_compose_run:
	docker-compose up -d --build
docker_compose_stop:
	docker-compose -f docker-compose.yml down
docker_rm_volumes:
	docker volume rm weather_forecast_database-data
docker_rm_images:
	docker image rm weather_forecast-webserver

