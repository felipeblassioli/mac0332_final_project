from fabric.api import *

def bootstrap():
    run('mkdir -p /var/www/funilaria')
    with cd('/var/www/funilaria'):
        run('virtualenv env')
        run('. env/bin/activate')
        put('config/funilaria.wsgi','funilaria.wsgi')
        put('config/funilaria.cfg.dev','funilaria.cfg')
    put('config/funilaria.vhost.dev', '/etc/apache2/sites-available/funilaria', use_sudo=True, mirror_local_mode=True)
    run('sudo a2ensite funilaria')
    # create database
    # mysql -u user --password=pwd -e "CREATE DATABASE dbname"
    _awk_script = """awk 'BEGIN { FS=":"; } { gsub(/[ ,"\\047"]/,"",$2); if (/name/) name=$2; if(/user/) user=$2; if(/passwd/) pwd=$2; } END { print "mysql -u" user, "--password=" pwd, "-e \\"CREATE DATABASE", name "\\""; }' %s """
    params=local(_awk_script % 'config/funilaria.cfg.dev',capture=True)
    run('mysql %s' % params, quiet=True)


def pack():
    local('python setup.py sdist --formats=gztar', capture=False)

def deploy():
    dist = local('python setup.py --fullname', capture=True).strip()
    put('dist/%s.tar.gz' % dist, '/tmp/funilaria.tar.gz')
    run('mkdir -p /tmp/funilaria')

    with cd('/tmp/funilaria'):
        run('tar xzf /tmp/funilaria.tar.gz')
        with cd('/tmp/funilaria/%s' % dist):
            run('/var/www/funilaria/env/bin/python setup.py install')
    run('rm -rf /tmp/funilaria /tmp/funilaria.tar.gz')
    run('sudo service apache2 reload')