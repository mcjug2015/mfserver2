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


def refresh_local():
    _ensure_virtualenv()
    install_prod_deps()


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
    local("""sudo docker exec %s sh /tmp/mfserver2/provisioning/misc/do_salt.sh""" % container_id)
    #sudo_docker_stop_remove()


def sudo_docker_stop_remove():
    with warn_only():
        local("""sudo docker stop $(sudo docker ps -a -q)""")
        local("""sudo docker rm $(sudo docker ps -a -q)""")
        # local("""sudo docker rmi -f $(sudo docker images -q)""")
