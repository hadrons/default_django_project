#coding: utf-8
import os

REPO_URL = 'git@bitbucket.org:hadrons/name_project.git'
NAME_PROJECT = 'name_project'
IP_SERVER = '111.111.111.111'


def rename_files():
    os.rename('config/deploy_config/default_nginx.conf', 
        'config/deploy_config/'+ NAME_PROJECT +'_nginx.conf')
    os.rename('config/deploy_config/default_supervisor.conf', 
        'config/deploy_config/'+ NAME_PROJECT +'_supervisor.conf')

def replace_text(filename):
    file = open('config/deploy_config/'+ filename)
    olddata = file.read()
    file.close()

    newdata = olddata.replace('NAME_PROJECT', NAME_PROJECT).replace('IP_SERVER', IP_SERVER)
    file = open('config/deploy_config/'+ filename, 'w')
    file.write(newdata)
    file.close()

def replace_text_nginx():
    replace_text('default_nginx.conf')

def replace_text_supervisor():
    replace_text('default_supervisor.conf')

def replace_text_gunicorn():
    replace_text('gunicorn_start.bash')

def replace_text_deploy_rb():
    file = open('config/deploy.rb')
    olddata = file.read()
    file.close()

    newdata = olddata.replace('NAME_PROJECT', NAME_PROJECT).replace('REPO_URL', REPO_URL)
    file = open('config/deploy.rb', 'w')
    file.write(newdata)
    file.close()

def replace_text_stages():
    file = open('config/deploy/production.rb')
    olddata = file.read()
    file.close()

    newdata = olddata.replace('IP_SERVER', IP_SERVER)
    file = open('config/deploy/production.rb', 'w')
    file.write(newdata)
    file.close()


if __name__ == '__main__':
    '''
        @config_project: Script for rename and replace names the configuration
    '''

    print('Initializing script')

    replace_text_nginx()
    replace_text_supervisor()
    replace_text_gunicorn()
    replace_text_deploy_rb()
    replace_text_stages()
    rename_files()


    print ('Script finished')