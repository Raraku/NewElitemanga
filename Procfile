release : python manage.py migrate --settings=elitemanga.settings.prod_heroku
web: bin/start-nginx gunicorn -c gunicorn.conf elitemanga.wsgi --log-file -