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

Cmnd_Alias FABRIC = /usr/bin/apt-get, /usr/bin/tee, /usr/bin/service, /usr/bin/psql, /usr/bin/createdb, /usr/bin/createlang
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
    env.warn_only=True
    run("sudo -u postgres createdb -E UTF8 -U postgres template_postgis")
    run("sudo -u postgres createlang -d template_postgis plpgsql;")
    run("sudo -u postgres psql -U postgres -d template_postgis -c \"CREATE EXTENSION hstore;\" ")
    env.warn_only=False
    run("sudo -u postgres psql -U postgres -d template_postgis -f /usr/share/postgresql/9.1/contrib/postgis-1.5/postgis.sql")
    run("sudo -u postgres psql -U postgres -d template_postgis -f /usr/share/postgresql/9.1/contrib/postgis-1.5/spatial_ref_sys.sql")
    run("sudo -u postgres psql -U postgres -d template_postgis -c \"select postgis_lib_version();\" ")
    run("sudo -u postgres psql -U postgres -d template_postgis -c \"GRANT ALL ON geometry_columns TO PUBLIC;\" ")
    run("sudo -u postgres psql -U postgres -d template_postgis -c \"GRANT ALL ON spatial_ref_sys TO PUBLIC;\" ")
    run("sudo -u postgres psql -U postgres -d template_postgis -c \"GRANT ALL ON geography_columns TO PUBLIC;\" ")
    run("echo 'Done!'")

def install_postgres():
    run('sudo apt-get install postgresql-9.1')
    run('sudo apt-get install postgresql-server-dev-9.1')
    run('sudo apt-get install postgresql-9.1-postgis')
    run('sudo apt-get install python-psycopg2')
    run('sudo service postgresql start')

def install_prerequirements():
    run('sudo apt-get install git')
    run('sudo apt-get install gcc')
    run('sudo apt-get install python-dev')
    run('sudo apt-get install python-virtualenv')
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


