namespace :setup do

    desc "Atualizacao e instalacao de depedencias para o projeto"
    task :install_requirements_server do
      on roles(:app) do
        execute "echo '==================== Install dependencies ===================='"

        execute "curl -sL https://deb.nodesource.com/setup_5.x | sudo -E bash -"
        execute "sudo apt-get update -y"
        execute "sudo apt-get install build-essential -y"
        execute "sudo apt-get -y install python-pip python-dev python2.7-dev python-virtualenv postgresql postgresql-contrib libpq-dev nginx supervisor git ssh libjpeg-dev zlib1g-dev libpng12-dev curl"
        execute "sudo apt-get -y install libtiff5-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk"
        execute "sudo apt-get install supervisor -y"
        execute "sudo apt-get install nginx -y"
        execute "sudo locale-gen"

        execute "sudo apt-get install -y nodejs"
        execute "npm install -g bower sass gulp"
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
        execute "mkdir #{fetch(:deploy_to)}/media"
        execute "mkdir #{fetch(:deploy_to)}/static_collected"
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
        #execute "cd #{fetch(:deploy_to)}/current/ && npm install && bower install --allow-root && gulp build"
        execute "#{fetch(:deploy_to)}/bin/python #{fetch(:deploy_to)}/current/manage.py collectstatic -v0 --noinput --settings=#{fetch(:application)}.settings_production"
      end
    end

    desc 'Notify service of deployment'
    task :notify do
      run_locally do
        with rails_env: :development do
          rake 'service:notify'
        end
      end
    end

end