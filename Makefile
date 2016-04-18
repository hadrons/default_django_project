clean:
	find . -name "*.pyc" -exec rm -rf {} \;
run: clean
	python manage.py runserver 0.0.0.0:8000
migrate:
	python manage.py migrate
migrations:
	python manage.py makemigrations
install:
	npm install
	bower install
	pip install -r requirements.txt
	make migrate
user:
	python manage.py createsuperuser

shell:
	python manage.py shell

tests: clean
	python manage.py test --settings=default.settings_tests

run_celery:
	celery worker -l info --beat --app=golegal.celery:app
	
initial_deploy:
	cap production setup:install_requirements_server
	cap production deploy
	cap production setup:create_folders
	cap production setup:install_requirements
	cap production setup:conf_files
	cap production setup:migrations
	cap production setup:collect_static
	cap production setup:restart_app
	

deploy:
	cap production deploy
	cap production setup:migrations
	cap production setup:collect_static
	cap production setup:restart_app