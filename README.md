# apiApp
 
# local setup
## Ensure to point the DB to local DB
1. git clone https://github.com/GoverdhanReddyGarudaiah/django_firstcut.git
2. cd django_firstcut
3. pip install -r requirements.txt
4. python3 manage.py makemigrations
5. python3 manage.py migrate
6. python3 manage.py runserver
# local setup




# aws EC2 Setup
1. connect to aws EC2 instance using ssh
2. sudo apt update
3. sudo apt install python3-pip python3-dev nginx
4. sudo apt install python3-venv (not required)
5. sudo apt install python3-virtualenv
6. git clone https://github.com/GoverdhanReddyGarudaiah/django_firstcut.git
7. cd django_firstcut
8. virtualenv env
9. source env/bin/activate
10. pip install -r requirements.txt
11. python3 manage.py makemigrations
12. python3 manage.py migrate
13. python3 manage.py collectstatic
14. deactivate
15. cd ..

# gunicorn setup
16. sudo vim /etc/systemd/system/gunicorn.socket
# write the following to socket file:
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target


10. sudo vim /etc/systemd/system/gunicorn.service
# write the following to service file:
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/django_firstcut
ExecStart=/home/ubuntu/django_firstcut/env/bin/gunicorn --access-logfile - --workers 3 --bind unix:/run/gunicorn.sock backend.wsgi:application

[Install]
WantedBy=multi-user.target

11. sudo systemctl start gunicorn.socket
12. sudo systemctl enable gunicorn.socket

# nginx setup
## Check for existing nginx config files
13. cd /etc/nginx/sites-available/
14. sudo rm -f default
15. cd ~

16. sudo vim /etc/nginx/sites-available/backend  
# write the following to nginx file:

server {
    listen 80 default_server;
    server_name _;
    location = /favicon.ico { access_log off; log_not_found off; }
    location /staticfiles/ {
        root /home/ubuntu/django_firstcut;
    }
    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}

17. sudo ln -s /etc/nginx/sites-available/backend /etc/nginx/sites-enabled

18. sudo gpasswd -a www-data ubuntu
19. sudo systemctl restart nginx
20. sudo systemctl restart gunicorn
22. sudo service gunicorn restart
23. sudo service nginx restart

24. sudo service nginx status
25. sudo service gunicorn status


## Django api flow
1. start app: python3 manage.py startapp <app_name>
2. define models in models.py
3. define serializers in serializers.py
4. define views in views.py
5. define urls in urls.py
6. add urls in project urls.py
