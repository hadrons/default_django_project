# Development Install

@todo

# Deploy

## First time

1. Install your key in the server.
2. Enable your key in the project repository.
3. Set ```config/deploy.rb``` variables properly.
3. Change files configuration:
    Rename ```config/deploy_config/*_nginx.conf``` files to match ```config_application_name``` variable set in ```config/deploy.rb```
4. Config database in the server.
    ```bash
    $ su - postgres
    $ psql
    psql$ CREATE DATABASE databasename;
    psql$ CREATE USER username WITH PASSWORD userpassword;
    psql$ GREANT ALL PRIVILEGES ON DATABASE databasename TO username;
    psql$ \q
    $ exit
    ```
5. Run ```make initial_deploy stage=production``` or whatever stage you eant deploy to.

# Config Celery


1. Install rabbitmq
    - Linux: sudo apt-get install rabbitmq-server 
    - Mac: brew install rabbitmq

2. Add user rabbitmq
    - sudo rabbitmqctl add_user myuser mypassword
    - sudo rabbitmqctl add_vhost myvhost
    - sudo rabbitmqctl set_permissions -p myvhost myuser ".*" ".*" ".*"

3. Install celery
    - pip install celery

# Celery Local
4. Run rabbitmq 
    - sudo rabbitmq-server

5. Run celery
    - celery worker -l info --beat --app=default.celery:app

# Celery Production

6. Create symlink to ../default/config/deploy_config/default_celery_supervisor.conf >> /etc/supervisor/conf.d/default_celery_supervisor.conf

7. Restart supervisorctl
