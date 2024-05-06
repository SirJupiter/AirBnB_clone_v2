#!/usr/bin/python3
"""Fabric script (based on the file 2-do_deploy_web_static.py)
creates and distributes an archive to your web servers,
using the function deploy"""

import os
from datetime import datetime
from fabric.api import local, run, put, env
# do_pack = __import__('1-pack_web_static').do_pack
# do_deploy = __import__('2-do_deploy_web_static').do_deploy

# Set Fabric environment variables
env.hosts = ['54.145.81.146', '18.207.234.98']  # servers addresses
env.user = 'ubuntu'
env.key_filename = '~/.ssh/school'


def do_pack():
    """Generates .tgz archive from the contents of web_static folder

    Return:
        archive created if properly created
        None in case of error
    """
    time = datetime.now()
    year = time.year
    month = time.month
    day = time.day
    hour = time.hour
    minute = time.minute
    sec = time.second
    darchive = f"versions/web_static_{year}{month}{day}{hour}{minute}{sec}.tgz"

    local('mkdir -p versions')
    created = local(f'tar -cvzf {darchive} web_static')

    if created.failed:
        return None

    return darchive


def do_deploy(archive_path):
    """Distributes an archive to my web servers

    Returns:
        True if all operations executed correctly
        False otherwise
    """
    if not os.path.exists(archive_path):
        return False

    try:
        file = archive_path.split('/')[1]
        web_dir = file.split('.')[0]

        put(archive_path, "/tmp/")

        new_path = f"/data/web_static/releases/{web_dir}/"

        run(f"mkdir -p {new_path}")

        run(f"tar -xvzf /tmp/{file} -C {new_path}")

        run(f"rm /tmp/{file}")

        run(f"mv {new_path}/web_static/* {new_path}")

        run(f"rm -rf {new_path}/web_static")

        run("rm -rf /data/web_static/current")

        run(f"ln -s {new_path} /data/web_static/current")

        return True
    except Exception:
        return False


def deploy():
    """Creates and distributes archive to web

    Returns:
        The return value of do_deploy()
    """

    archive_path = do_pack()
    if archive_path is None:
        return False

    # return_val = do_deploy(archive_path)
    # return return_val
