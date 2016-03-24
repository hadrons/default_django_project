namespace :setup do

    desc "Atualizacao e instalacao de depedencias para o projeto"
    task :install_requirements_server do
      on roles(:app) do
        execute "echo '==================== Install dependencies ===================='"

        execute "sudo apt-get update -y"
        execute "sudo apt-get install build-essential -y"
        execute "sudo apt-get -y install python-pip python-dev python2.7-dev python-virtualenv postgresql postgresql-contrib libpq-dev nginx supervisor git ssh libjpeg-dev zlib1g-dev libpng12-dev curl"
        execute "sudo apt-get install supervisor -y"
        execute "sudo apt-get install nginx -y"
        execute "sudo locale-gen"

        execute "curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.30.1/install.sh | bash"
        execute "source ~/.bashrc && sudo update-locale LC_ALL='en_US.UTF-8'"
        execute "source ~/.nvm/nvm.sh && nvm install 0.12"
        execute "nvm alias default stable"
        execute "npm install"
      end
    end


    task :create_folders do
      on roles(:app) do
        execute "echo '==================== Create folders log ===================='"
        execute "cd /home/webapps/ && virtualenv #{fetch(:deploy_to)} --no-site-package"
        execute "mkdir #{fetch(:deploy_to)}/shared/log/"
        execute "touch #{fetch(:deploy_to)}/shared/log/nginx-access.log"
        execute "touch #{fetch(:deploy_to)}/shared/log/nginx-error.log"
        execute "touch #{fetch(:deploy_to)}/shared/log/gunicorn_supervisor.log"
        execute "mkdir /home/webapps/media"
        execute "mkdir /home/webapps/static_collected"
      end
    end

    desc "Install requirements"
    task :install_requirements do
      on roles(:app) do
        execute "echo '==================== Install requirements project ===================='"
        execute "source #{fetch(:deploy_to)}/bin/activate"
        execute "#{fetch(:deploy_to)}/bin/pip install -r #{fetch(:deploy_to)}/current/requirements_production.txt"
      end
    end
    task :"migrations" do
      on roles(:app) do
        execute "echo '==================== Running migrations ===================='"
        execute "source #{fetch(:deploy_to)}/bin/activate"
        execute "#{fetch(:deploy_to)}/bin/python #{fetch(:deploy_to)}/current/manage.py migrate --settings=#{fetch(:application)}.settings_production"
      end
    end
    task :"conf_files" do
      on roles(:app) do
        execute "sudo ln -s -f #{fetch(:deploy_to)}/current/config/deploy_config/#{fetch(:application)}_nginx.conf /etc/nginx/sites-enabled/#{fetch(:application)}_nginx.conf"
        execute "sudo service nginx reload"
        execute "sudo ln -s -f #{fetch(:deploy_to)}/current/config/deploy_config/#{fetch(:application)}_supervisor.conf /etc/supervisor/conf.d/#{fetch(:application)}_supervisor.conf"
        execute "sudo service supervisor restart"
      end
    end

    desc "Restart application"
    task :restart_app do
      on roles(:app) do
        execute "echo '==================== Restart application ===================='"
        execute "sudo supervisorctl reread && sudo supervisorctl update"
        execute "sudo supervisorctl restart all"
        execute "sudo service nginx reload"
      end
    end


    desc "Collectstatic"
    task :collect_static do
      on roles(:app) do
        execute "echo '==================== Collectstatic ===================='"
        execute "source ~/.nvm/nvm.sh && cd #{fetch(:deploy_to)}/current/ && npm install && bower install --allow-root && gulp build"
        execute "#{fetch(:deploy_to)}/bin/python #{fetch(:deploy_to)}/current/manage.py collectstatic -v0 --noinput --settings=#{fetch(:application)}.settings_production"
      end
    end

end