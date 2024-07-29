# sudo docker-compose up --build -d --force-recreate
sudo docker compose down -v
sudo docker compose up --build -d --remove-orphans --force-recreate
