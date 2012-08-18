__author__ = 'maxim'

from fabric.contrib import files
from fabric.api import *
from datetime import datetime

env.hosts=['127.0.0.1']
env.user='maxim'
env.password=''
env.project='arp_v2'
env.env='.venv'
env.repo='git://github.com/shamanu4/arp_v2.git'

"""

# /etc/sudoers setup:
# add these lines to allow execute required commands without password

Cmnd_Alias FABRIC = /usr/bin/yum, /usr/bin/tee, /sbin/chkconfig, /sbin/service, /usr/bin/psql
fabric		ALL=(ALL)	NOPASSWD: FABRIC

"""

import os, sys

def rel(*x):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)

sys.path.insert(0, rel('lib'))
sys.path.insert(0, rel('.',))
sys.path.insert(0, rel('..',))

now = datetime.now()
timestamp='%s-%s-%s-%s-%s' % (now.year, now.month, now.day, now.hour, now.minute)

def host_type():
    run('uname -s')

def install_postgis():
    repo_descr="""
[pgdg90]
name=PostgreSQL 9.0 $releasever - $basearch
baseurl=http://yum.pgrpms.org/9.0/redhat/rhel-$releasever-$basearch
enabled=1
gpgcheck=0
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-PGDG
[pgdg90-source]
name=PostgreSQL 9.0 $releasever - $basearch - Source
failovermethod=priority
baseurl=http://yum.pgrpms.org/srpms/9.0/redhat/rhel-$releasever-$basearch
gpgcheck=0
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-PGDG
    """
    run("echo '%s' | sudo tee /etc/yum.repos.d/pgrpms9.repo" % repo_descr)
    run("sudo yum install postgis90")
    run("sudo -u postgres bash lib/postgis/create_template_postgis-1.5.sh")

def install_postgres():
    run('sudo yum install postgresql90-devel')
    run('sudo yum install postgresql-devel')        # postgresql90-devel has not pg_config
    run('sudo yum install postgresql90-server')
    run('sudo yum install postgresql-python')
    run('sudo chkconfig --add postgresql-9.0')
    run('sudo service postgresql-9.0 initdb')
    run('sudo chkconfig postgresql-9.0 on')
    run('sudo service postgresql-9.0 start')

def install_prerequirements():
    run('sudo yum install wget')
    run('sudo yum install gcc')
    run('sudo yum install git')
    #run('sudo yum install mysql-devel')
    run('sudo yum install python-devel')
    run('sudo yum install libxml2-devel')
    run('sudo yum install libxslt-devel')
    run('sudo yum install binutils')
    install_postgres()
    install_postgis()

def create_environ():
    with cd(env.project):
        run('virtualenv %s' % (env.env,))

def install_requirements():
    with cd(env.project):
        with prefix('source %s/bin/activate' % env.env):
            run('pip install -r requirements.txt')

def backup_project():
    if files.exists(env.project):
        run('tar -cvzf %s-%s.tgz %s' % (env.project, timestamp, env.project))
        #run('rm -rf %s' % (env.project,))

def install_project():
    if files.exists(env.project):
        run('git pull')
    else:
        run('git clone %s' % (env.repo,))
    create_environ()

def copy_local_settings():
    if env.host_string == "127.0.0.1" or env.host_string == "localhost":
        if not os.path.isfile("src/local_settings.py"):
            #local("cp src/local_settings.py src/local_settings.py.b")
            local("cp src/local_settings.dist.py local_settings.py")
    else:
        if files.exists("local_settings.py"):
            put("local_settings.py", "~/%s/src" % (env.project,))
        else:
            print run("pwd")
            if not files.exists("local_settings.py"):
                if not os.path.isfile("src/local_settings.py"):
                    put("local_settings.dist.py", "~/%s/src/local_settings.py" % (env.project,))
                else:
                    put("local_settings.py", "~/%s/src/local_settings.py" % (env.project,))

def backup_db(db):
    env.warn_only=True
    run('sudo -u postgres pg_dump %s > %s.%s.sql' % (db,db,timestamp) )
    env.warn_only=False

def create_db(db,user,password):
    run('sudo -u postgres psql -c "DROP DATABASE IF EXISTS %s;"' % (db,) )
    run('sudo -u postgres psql -c "DROP USER IF EXISTS %s;"' % (user,) )
    run('sudo -u postgres psql -c "CREATE USER %s WITH PASSWORD \'%s\';"' % (user,password) )
    run('sudo -u postgres psql -c "CREATE DATABASE %s OWNER %s TEMPLATE=template_postgis;"' % (db,user))

def setup_db():
    from src.local_settings import DATABASES
    for i in DATABASES:
        db = DATABASES[i]
        if db['ENGINE'] == 'django.contrib.gis.db.backends.postgis':
            backup_db(db['NAME'])
            create_db(db['NAME'],db['USER'],db['PASSWORD'])

def syncdb():
    with cd(env.project):
        with prefix('source %s/bin/activate' % env.env):
            with prefix("cd src"):
                run("python manage.py syncdb")

def setup():
    """
    This function initializes new project.
    If old project directory found it will be backed-up in archive
    """
    install_prerequirements()
    backup_project()
    install_project()
    install_requirements()
    copy_local_settings()
    setup_db()

def pull(branch='master'):
    with cd(env.project):
        with prefix('source %s/bin/activate' % env.env):
            run('git pull origin %s' % branch)


