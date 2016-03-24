set :stages, %w(starting)
set :default_stage, "starting"
require 'capistrano/ext/multistage'

set :application, "laville"

set :repository,  "git@git.hadrons.io:hadrons/lavillekids-invitations.git"
set :branch, "master"
#set :repository,  "."

set :user, "root"
set :use_sudo, true

set :deploy_to, "/home/webapps/#{application}"
#set :deploy_via, :copy

set :copy_dir, "/tmp"
set :copy_remote_dir, "/tmp"

set :copy_exclude, [".git", ".gitignore", "*.pyc", "**/.git", "**/*.log", "**/.pyc", ".swp", ".swp", "Gemfile", "tmp/", '**/.gitignore', 'Capfile', 'REVISION', 'Vagrant', 'Gemfile.lock', '**/Vagrant', '**/Capfile', '**/REVISION']



set :scm, :git
#set :scm, :none

set :keep_releases, 3

namespace :deploy do
	task :finalize_update do
	end

	task :restart_app do
		run "sudo supervisorctl reread && sudo supervisorctl update"
		run "sudo supervisorctl restart all"
	end

	task :restart_celery do
		run "sudo supervisorctl restart celery"
	end

	task :collectstatic do
		python_path = "#{deploy_to}/bin/python"
		run "#{python_path} #{deploy_to}/current/manage.py collectstatic -v0 --noinput --settings=laville.settings_production"
	end

	desc "Atualizacao e instalacao de depedencias para o projeto"
	task :setup do
		path_files = '/home/webapps'

		run "echo Setup Server"
		run "sudo rm -rf /home/webapps/#{application}"
		run "sudo mkdir -p /home/webapps/laville /home/webapps/laville/releases /home/webapps/laville/shared /home/webapps/capuri/shared/system /home/webapps/capuri/shared/log /home/webapps/capuri/shared/pids"
		run "sudo chmod g+w /home/webapps/laville /home/webapps/laville/releases /home/webapps/laville/shared /home/webapps/laville/shared/system /home/webapps/laville/shared/log /home/webapps/laville/shared/pids"
		run "echo Atualizando"
		run "sudo apt-get update -y"
		run "sudo apt-get -y install python-dev python2.7-dev python-virtualenv postgresql postgresql-contrib libpq-dev nginx supervisor git ssh libjpeg-dev zlib1g-dev libpng12-dev"
		run "sudo ln -s -f #{deploy_to}/shared/log/ #{deploy_to}/logs"
		run "echo Configurando"
		run "cd #{deploy_to} && virtualenv . "
		run "mv -f #{path_files}/gunicorn_start.bash #{deploy_to}/bin/"
		run "chmod u+x #{deploy_to}/bin/gunicorn_start.bash"
		run "mv -f #{path_files}/laville.conf /etc/nginx/sites-enabled/"
		run "sudo ln -s -f /etc/nginx/sites-enabled/laville.conf /etc/nginx/sites-available/laville.conf"
		run "mv -f #{path_files}/laville_supervisor.conf /etc/supervisor/conf.d/"
		run "sudo chown -h webapps:webapps /home/webapps/laville/* && sudo chown -h webapps:webapps /home/webapps/laville/shared/log/"
		run "ssh-keyscan -t rsa git.hadrons.io >> ~/.ssh/known_hosts"
		run "sudo service ssh restart"

	end

	task :restart, :roles => :app do
		python_path = "#{deploy_to}/bin/python"
		run "#{deploy_to}/bin/pip install -r #{deploy_to}/current/requirements_production.txt"
		run "#{python_path} #{deploy_to}/current/manage.py migrate --settings=laville.settings_production"
		run "rm #{deploy_to}/current/**/migrations/*[0-9]*.py && rm #{deploy_to}/current/**/migrations/*[0-9]*.pyc"
		run "#{python_path} #{deploy_to}/current/manage.py makemigrations --settings=laville.settings_production"
		run "#{python_path} #{deploy_to}/current/manage.py collectstatic -v0 --noinput --settings=laville.settings_production"
		#run "cd #{deploy_to}/current && sudo npm install && bower install --allow-root"
		run "sudo supervisorctl reread"
		run "sudo supervisorctl restart laville"
		run "sudo service nginx restart"

	end
end