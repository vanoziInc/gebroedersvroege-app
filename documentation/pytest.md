# Run unit tests with standard output
docker-compose -f docker-compose-dev.yml --env-file .env.dev exec fastapi python -m pytest -v -m unittest

# pytest cov + parallel
docker-compose -f docker-compose-dev.yml --env-file .env.dev exec fastapi python -m pytest --cov=app tests/
