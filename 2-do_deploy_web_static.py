#!/usr/bin/python3
"""script (based on the file 1-pack_web_static.py)
distributes an archive to your web servers, using the function do_deploy"""

import os
from fabric.api import run, put, env

# Set Fabric environment variables
env.hosts = ['54.145.81.146', '18.207.234.98']  # servers addresses
env.user = 'ubuntu'
env.key_filename = '~/.ssh/school'


def do_deploy(archive_path):
    """Distributes an archive to my web servers

    Returns:
        True if all operations executed correctly
        False otherwise
    """
    if not os.path.exists(archive_path):
        return False

    try:
        file_n = archive_path.split("/")[-1]
        no_ext = file_n.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run('mkdir -p {}{}/'.format(path, no_ext))
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_n, path, no_ext))
        run('rm /tmp/{}'.format(file_n))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, no_ext))
        run('rm -rf {}{}/web_static'.format(path, no_ext))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, no_ext))
        return True
    except Exception:
        return False
