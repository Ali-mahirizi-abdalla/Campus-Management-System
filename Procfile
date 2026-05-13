web: gunicorn swms.wsgi --log-file -
worker: celery -A swms worker --loglevel=info
beat: celery -A swms beat --loglevel=info
