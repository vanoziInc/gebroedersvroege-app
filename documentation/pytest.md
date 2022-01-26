# Run backend tests
docker exec fastapi python -m pytest --verbose --cov=app --cov-report html:cov_html --cov-config=tests/.coveragerc -m "apitest or unittest" --html=backend-test-report.html --self-contained-html --force-sugar

# Run frontend tests
pytest ./backend/tests/frontend/ --html=frontend-test-report.html --self-contained-html