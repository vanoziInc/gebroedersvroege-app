
<!-- Setup Aerich -->
aerich init -t app.db.TORTOISE_ORM

aerich init-db


docker-compose -f docker-compose-dev.yml exec web aerich init -t app.db.TORTOISE_ORM