release: python manage.py migrate
web: gunicorn ChatApp.wsgi --log-file - --log-level debug
