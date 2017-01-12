import os
import sys
from fabric.api import env, local
from fabric.context_managers import warn_only


def _ensure_virtualenv():
    if "VIRTUAL_ENV" not in os.environ:
        sys.stderr.write("$VIRTUAL_ENV not found. Make sure to activate virtualenv first\n\n")
        sys.exit(-1)
    env.virtualenv = os.environ["VIRTUAL_ENV"]


def install_prod_deps():
    _ensure_virtualenv()
    local('pip install -q -r dependencies/pip/prod.txt')


def install_dev_deps():
    _ensure_virtualenv()
    local('pip install -q -r dependencies/pip/dev.txt')


def pep8():
    _ensure_virtualenv()
    local('pep8 --config=conf_dev/pep8/pep8_config.txt django_app')
    local('pep8 --config=conf_dev/pep8/pep8_config.txt django_proj')


def pylint():
    _ensure_virtualenv()
    local('pylint --rcfile=conf_dev/pylint/pylintrc.txt django_app')
    local('pylint --rcfile=conf_dev/pylint/pylintrc.txt django_proj')


def run_tests():
    _ensure_virtualenv()
    local('coverage erase')
    local('coverage run --branch manage.py test')
    local('coverage html -d py_coverage --include=django_app/*')
    local('coverage report -m --fail-under=100 --include=django_app/* --omit=django_app/migrations/*')


def precommit():
    _ensure_virtualenv()
    install_prod_deps()
    install_dev_deps()
    pep8()
    pylint()
    run_tests()


def update_static_files():
    local('rm -rf /opt/mfserver2/static/')
    local('mkdir -p /opt/mfserver2/static/')
    local('cp -r /opt/mfserver2/venv/lib/python2.7/site-packages/django/contrib/admin/static/admin /opt/mfserver2/static/')
    local('cp -r /opt/mfserver2/venv/lib/python2.7/site-packages/django/contrib/gis/static/gis /opt/mfserver2/static/')


def refresh_local():
    _ensure_virtualenv()
    install_prod_deps()
    local("""python manage.py migrate""")
    update_static_files()


def sudo_docker_provision():
    local("""rm -rf dist""")
    local("""mkdir -p dist""")
    local("""tar --exclude='dist' --exclude='.git' -czf  dist/mfserver2.tar.gz *""")
    local("""sudo docker build --rm -t local/c7-systemd provisioning/docker/c7-systemd""")
    local("""sudo docker build --rm -t local/c7-mfserver2 provisioning/docker/c7-mfserver2""")
    container_id = local("""sudo docker run --privileged -d -t -v /sys/fs/cgroup:/sys/fs/cgroup:ro -p 80:80 -p 443:443 -p 8000:8000 local/c7-mfserver2""", capture=True)
    local("""sudo docker cp dist/mfserver2.tar.gz %s:/root""" % container_id)
    local("""sudo docker exec %s mkdir -p /tmp/mfserver2""" % container_id)
    local("""sudo docker exec %s tar -xzf /root/mfserver2.tar.gz -C /tmp/mfserver2""" % container_id)
    local("""sudo docker exec -t %s sh /tmp/mfserver2/provisioning/misc/do_salt.sh""" % container_id)
    local("""curl -f -k https://127.0.0.1/mfserver2/welcome/""")
    #sudo_docker_stop_remove()


def sudo_docker_stop_remove():
    with warn_only():
        local("""sudo docker stop $(sudo docker ps -a -q)""")
        local("""sudo docker rm $(sudo docker ps -a -q)""")
        #local("""sudo docker rmi -f $(sudo docker images -q)""")
        pass


def sudo_refresh_local():
    sudo_update_ngnix_confs()
    sudo_copy_uwsgi_ini()
    sudo_put_root_uwsgi_ini()
    sudo_put_uwsgi_systemd_file()
    sudo_reboot_all()


def sudo_update_ngnix_confs():
    local('sudo cp conf/nginx/nginx.conf /etc/nginx/')
    local('sudo cp conf/nginx/mfserver2.conf /etc/nginx/conf.d/')


def sudo_copy_uwsgi_ini():
    local('sudo cp conf/uwsgi/uwsgi.ini /etc/uwsgi.d/' % env)
    local('sudo chown reg_user:reg_user /etc/uwsgi.d/uwsgi.ini' % env)


def sudo_put_root_uwsgi_ini():
    local("sudo cp conf/uwsgi/root_uwsgi.ini /etc/uwsgi.ini")


def sudo_put_uwsgi_systemd_file():
    local("sudo cp conf/uwsgi/uwsgi.service /usr/lib/systemd/system/uwsgi.service")
    local("sudo systemctl enable uwsgi")
    local("sudo systemctl daemon-reload")


def sudo_reboot_all():
    with warn_only():
        local('sudo systemctl stop nginx')
        local('sudo systemctl stop uwsgi')
    local('sudo systemctl start uwsgi')
    local('sudo systemctl start nginx')
