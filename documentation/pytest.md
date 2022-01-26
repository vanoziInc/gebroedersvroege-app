# Run backend tests
docker exec fastapi python -m pytest --verbose --cov=app --cov-report html:cov_html --cov-config=tests/.coveragerc -m "apitest or unittest" --html=backend-test-report.html --self-contained-html --force-sugar

# pytest cov + parallel
docker-compose -f docker-compose-dev.yml --env-file .env.dev exec fastapi python -m pytest --cov=app tests/

# run frontend tests
docker build -t playwright-tests ./frontend-testing/.
docker run -t playwright-tests