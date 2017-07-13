(flask run)
(redis-server)
(celery flower -A tasks)
(celery -A tasks worker --loglevel=info)
