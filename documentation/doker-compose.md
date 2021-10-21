# dev
docker-compose --env-file .env.dev up

docker-compose -f docker-compose-dev.yml --env-file .env.dev up

docker-compose -f docker-compose-prod.yml --env-file .env.prod up -d