release: flask db upgrade
web: gunicorn --worker-tmp-dir /dev/shm --bind 0.0.0.0:$PORT --workers 3 autoapp:app
