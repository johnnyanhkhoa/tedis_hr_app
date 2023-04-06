python manage.py makemigrations
python manage.py migrate
sudo systemctl daemon-reload
sudo systemctl restart gunicorn 