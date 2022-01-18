# dev
docker-compose --env-file .env.dev up

docker-compose -f docker-compose-dev.yml --env-file .env.dev up

docker-compose -f docker-compose-prod.yml --env-file .env.prod up -d

# testing
docker-compose -f docker-compose-test.yml --env-file .env.test exec fastapi python -m pytest