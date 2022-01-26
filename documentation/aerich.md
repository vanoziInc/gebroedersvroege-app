
<!-- Setup Aerich -->
aerich init -t app.db.TORTOISE_ORM
aerich init-db
aerich migrate
aerich upgrade