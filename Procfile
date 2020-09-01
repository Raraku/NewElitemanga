release : python manage.py migrate
web: bin/start-nginx gunicorn -c gunicorn.conf elitemanga.wsgi --log-file -