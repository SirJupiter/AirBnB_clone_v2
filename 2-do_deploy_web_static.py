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

        print("New version deployed!")

        return True
    except Exception:
        return False
