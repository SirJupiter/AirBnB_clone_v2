#!/usr/bin/python3
"""script (based on the file 1-pack_web_static.py)
distributes an archive to your web servers, using the function do_deploy"""

import os
from fabric.api import run, put, env

# Set Fabric environment variables
env.hosts = ['54.145.81.146', '18.207.234.98']  # servers addresses
# env.user = 'ubuntu'
# env.key_filename = '~/.ssh/school'


def do_deploy(archive_path):
    """Distributes an archive to my web servers

    Returns:
        True if all operations executed correctly
        False otherwise
    """
    if not os.path.exists(archive_path):
        return False

    try:
        the_file = archive_path.split("/")[-1]
        no_ext = the_file.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run(f'mkdir -p {path}{no_ext}/')
        run(f'tar -xzf /tmp/{the_file} -C {path}{no_ext}/')
        run(f'rm /tmp/{the_file}')
        run(f'mv {path}{no_ext}/web_static/* {path}{no_ext}/')
        run(f'rm -rf {path}{no_ext}/web_static')
        run('rm -rf /data/web_static/current')
        run(f'ln -s {path}{no_ext}/ /data/web_static/current')
        return True
    except Exception:
        return False
