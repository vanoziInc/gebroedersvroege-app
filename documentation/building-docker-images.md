# Build postgres image
docker build -f project/db/Dockerfile -t docker.pkg.github.com/vaozi/<REPOSITORY_NAME>/summarizer:latest ./project


# Migrations
docker-compose -f docker-compose-dev.yml exec fastapi aerich init-db
docker-compose -f docker-compose-dev.yml exec fastapi aerich migrate