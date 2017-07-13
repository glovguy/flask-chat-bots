(flask run) &
(redis-server) &
(celery flower -A tasks) &
(celery -A tasks worker --loglevel=info) &
echo "\n\nAll apps started\n\n"