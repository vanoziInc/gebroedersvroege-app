# Run unit tests with standard output
docker-compose -f docker-compose-dev.yml --env-file .env.dev exec fastapi python -m pytest -v -m unittest
docker-compose -f docker-compose-test.yml --env-file .env.test exec fastapi python -m pytest -v -m unittest

# pytest cov + parallel
docker-compose -f docker-compose-dev.yml --env-file .env.dev exec fastapi python -m pytest --cov=app tests/

# run frontend tests
docker build -t playwright-tests ./frontend-testing/.
docker run -t playwright-tests