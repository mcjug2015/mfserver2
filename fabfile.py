hello victor


import os
import sys
from fabric.api import env, local
from fabric.context_managers import warn_only, lcd, shell_env
import time
from fabric.utils import abort
from time import sleep
from deleteme.scratchpad import do_something


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
    local('pycodestyle --config=conf_dev/pep8/pep8_config.txt django_app')
    local('pycodestyle --config=conf_dev/pep8/pep8_config.txt django_proj')
    local('pycodestyle --config=conf_dev/pep8/pep8_config.txt biz_int')


def pylint():
    _ensure_virtualenv()
    local('pylint --rcfile=conf_dev/pylint/pylintrc.txt django_app')
    local('pylint --rcfile=conf_dev/pylint/pylintrc.txt django_proj')
    local('pylint --rcfile=conf_dev/pylint/pylintrc.txt biz_int')


def run_tests():
    _ensure_virtualenv()
    local('rm -rf py_coverage')
    local('coverage erase')
    local('coverage run --branch manage.py test django_app.test')
    local('coverage html -d py_coverage --include=django_app/*')
    local('coverage report -m --fail-under=100 --include=django_app/* --omit=django_app/migrations/* --omit=django_app/test_py_integration/*')


def run_py_integration_tests():
    _ensure_virtualenv()
    local("python manage.py test django_app.test_py_integration")


def precommit():
    _ensure_virtualenv()
    install_prod_deps()
    install_dev_deps()
    pep8()
    pylint()
    run_tests()
    run_py_integration_tests()


def sudo_update_static_files():
    local('sudo rm -rf /opt/mfserver2/static/')
    local('sudo mkdir -p /opt/mfserver2/static/')
    local('sudo cp -r /opt/mfserver2/venv/lib/python3.4/site-packages/django/contrib/admin/static/admin /opt/mfserver2/static/')
    local('sudo cp -r /opt/mfserver2/venv/lib/python3.4/site-packages/django/contrib/gis/static/gis /opt/mfserver2/static/')
    local('sudo chown -R reg_user:reg_user /opt/mfserver2/static/')


def refresh_local():
    _ensure_virtualenv()
    install_prod_deps()
    local("""python manage.py migrate""")


def sudo_docker_provision():
    local("""rm -rf dist""")
    local("""mkdir -p dist""")
    local("""tar --exclude='dist' --exclude='.git' -czf  dist/mfserver2.tar.gz *""")
    local("""sudo docker build --rm -t local/c7-mfserver2 provisioning/docker/c7-mfserver2""")
    container_id = local("""sudo docker run --privileged -d -t -v /sys/fs/cgroup:/sys/fs/cgroup:ro -p 80:80 -p 443:443 local/c7-mfserver2""", capture=True)
    local("""sudo docker cp dist/mfserver2.tar.gz %s:/root""" % container_id)
    local("""sudo docker exec %s mkdir -p /tmp/mfserver2""" % container_id)
    local("""sudo docker exec %s tar -xzf /root/mfserver2.tar.gz -C /tmp/mfserver2""" % container_id)
    local("""sudo docker exec -t %s sh /tmp/mfserver2/provisioning/misc/do_salt.sh""" % container_id)
    sleep(3)
    local("""curl -f -k https://127.0.0.1/mfserver2/welcome/""")
    # sudo_docker_stop_remove()
    pass


def sudo_docker_stop_remove():
    with warn_only():
        local("""sudo docker stop $(sudo docker ps -a -q)""")
        local("""sudo docker rm $(sudo docker ps -a -q)""")
        #if docker provisioning freezes while dling packages do this and try again:
        #local("""sudo docker rmi -f $(sudo docker images -q)""")
        pass


def sudo_refresh_local():
    sudo_update_static_files()
    sudo_update_ngnix_confs()
    sudo_copy_uwsgi_ini()
    sudo_put_root_uwsgi_ini()
    sudo_put_uwsgi_systemd_file()
    sudo_reboot_all()


def sudo_ensure_uwsgi_nginx_socket_dir():
    '''
        latest centos 7 with gnome seems to chew up socket folder on occasion,
        making sure its there.
    '''
    local('sudo mkdir -p /var/run/mfserver2')
    local('sudo chown -R reg_user:reg_user /var/run/mfserver2')


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
    sudo_ensure_uwsgi_nginx_socket_dir()
    local('sudo systemctl start uwsgi')
    local('sudo systemctl start nginx')


def create_do_box(do_token="", ssh_key_local_path="./../vb_key.pub",
                  ssh_key_do_name="Victors_vb_public_ssh_key"):
    with lcd("provisioning/terraform/do"):
        command = '''terraform plan -var "ssh_key_local_path=%s" -var "ssh_key_do_name=%s" -out the_plan''' % (ssh_key_local_path,
                                                                                                               ssh_key_do_name)
        if do_token:
            command += ''' -var "do_token=%s"''' % do_token
        local(command)
        local('''terraform apply the_plan''')
        local('''terraform show''')


def create_do_box_and_wait(do_token="",
                           ssh_key_local_path="./../vb_key.pub",
                           ssh_key_do_name="Victors_vb_public_ssh_key",
                           max_wait=720):
    ''' blocking create_do_box '''
    create_do_box(do_token, ssh_key_local_path, ssh_key_do_name)
    with lcd("provisioning/terraform/do"):
        ip_address = local("""terraform output ip""", capture=True)
        ip_address = ip_address.strip()
    output = ""
    timeout = time.time() + max_wait
    while time.time() < timeout and "Welcome to meeting finder server 2" not in output:
        with warn_only():
            output = local("""curl -k https://%s/mfserver2/welcome/""" % ip_address, capture=True)
        if "Welcome to meeting finder server 2" not in output:
            time.sleep(60)
    if "Welcome to meeting finder server 2" not in output:
        abort("Mfserver2 provisioning did not complete in %s seconds" % max_wait)


def destroy_do_box(do_token):
    with warn_only():
        with lcd("provisioning/terraform/do"):
            local('''terraform destroy -force -var "do_token=%s"''' % do_token)


def backup_local_db(output_dir="./"):
    meetings_file_path = os.path.join(output_dir, "mfserver2_backup.txt")
    schema_file_path = os.path.join(output_dir, "mfserver2_backup_schema.txt")
    data_file_path = os.path.join(output_dir, "mfserver2_backup_data.txt")
    with shell_env(PGPASSWORD='mfserver2'):
        local("""psql -h127.0.0.1 -Umfserver2 -dmfserver2 -c'select id, name, description, address, ST_AsText (geo_location), created_date from django_app_meeting' > %s""" % meetings_file_path)
        local("""pg_dump -h127.0.0.1 -Umfserver2 --schema=public --schema-only --no-owner --verbose --no-acl --column-inserts --quote-all-identifiers mfserver2 > %s""" % schema_file_path)
        local("""pg_dump -h127.0.0.1 -Umfserver2 --schema=public --data-only --no-owner --verbose --no-acl --column-inserts --quote-all-identifiers mfserver2 > %s""" % data_file_path)


def restore_local_db(schema_dump_path="mfserver2_backup_schema.dump",
                     data_dump_path="mfserver2_backup_data.dump"):
    with shell_env(PGPASSWORD='mfserver2'):
        with warn_only():
            local('''psql -h127.0.0.1 -Umfserver2 -c"SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'mfserver2';"''')
        local("""dropdb -h127.0.0.1 -Umfserver2 --if-exists mfserver2""")
        local("""createdb -h127.0.0.1 -Umfserver2 mfserver2""")
        local('''psql -h127.0.0.1 -Umfserver2 mfserver2 -c "CREATE EXTENSION postgis; CREATE EXTENSION postgis_topology;"''')
        local("""psql -h127.0.0.1 -Umfserver2 -dmfserver2 mfserver2 < %s""" % schema_dump_path)
        local("""psql -h127.0.0.1 -Umfserver2 -dmfserver2 mfserver2 < %s""" % data_dump_path)


def scratchpad():
    do_something()


if __name__ == '__main__':
    from fabric.main import main
    sys.argv = ['fab', '-f', __file__,] + sys.argv[1:]
    main()
