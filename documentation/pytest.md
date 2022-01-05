# Run pytest with standard output
docker-compose -f docker-compose-dev.yml --env-file .env.dev exec fastapi python -m pytest -s

# pytest cov + parallel
docker-compose -f docker-compose-dev.yml --env-file .env.dev exec fastapi python -m pytest --cov=app tests/
