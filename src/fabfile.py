__author__ = 'maxim'

from fabric import context_managers
from fabric.contrib import files
from fabric.api import *
from datetime import datetime

env.hosts=['192.168.33.91']
env.user='fabric'
env.password=''
env.project='arp_v2'
env.env='.venv'
env.repo='git://github.com/shamanu4/arp_v2.git'

def host_type():
    run('uname -s')

def install_prerequirements():
    try:
        run('git --version')
    except:
        run('sudo yum install git')

def install_requirements():
    with cd(env.project):
        with prefix('source %s/bin/activate' % env.env):
            run('pip install -r src/requirements.txt')

def init_project():
    """
    This function initializes new project.
    If old project directory found it will be backed-up in archive
    """
    install_prerequirements()
    if files.exists(env.project):
        now = datetime.now()
        timestamp='%s-%s-%s-%s-%s' % (now.year, now.month, now.day, now.hour, now.minute)
        run('tar -cvzf %s-%s.tgz %s' % (env.project, timestamp, env.project))
        run('rm -rf %s' % (env.project,))
    run('git clone %s' % (env.repo,))
    with cd(env.project):
        run('virtualenv %s' % (env.env,))
    install_requirements()



