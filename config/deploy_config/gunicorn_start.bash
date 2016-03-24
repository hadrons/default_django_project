#!/bin/bash
NAME="default" #Name app
DJANGODIR=/home/webapps/default/current/
SOCKFILE=/home/webapps/default/run/gunicorn.sock  # we will communicte using
NUM_WORKERS=3                                     # how many worker processes
DJANGO_SETTINGS_MODULE=default.settings_production             # which settings file should
DJANGO_WSGI_MODULE=default.wsgi                     # WSGI module name

# Activate the virtual environment
cd $DJANGODIR
source /home/webapps/default/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do
# not use --daemon)
exec /home/webapps/default/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
	--name $NAME \
	--workers $NUM_WORKERS \
	--bind=unix:$SOCKFILE \
	--log-level=debug \
	--log-file=-
