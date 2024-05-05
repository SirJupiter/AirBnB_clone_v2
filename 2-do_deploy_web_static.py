#!/usr/bin/python3
"""script (based on the file 1-pack_web_static.py)
distributes an archive to your web servers, using the function do_deploy"""

import os
from datetime import datetime
from fabric.api import local, run, put, env

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

    time = datetime.now()
    year = time.year
    month = time.month
    day = time.day
    hour = time.hour
    minute = time.minute
    sec = time.second
    darchive = f"web_static_{year}{month}{day}{hour}{minute}{sec}.tgz"

    local('mkdir -p versions')
    local(f'tar -cvzf versions/{darchive} web_static')

    upload = put(f"versions/{darchive}", "/tmp/")
    if upload.failed:
        return False

    new_path = f"/data/web_static/releases/{darchive[:-4]}"

    run(f"mkdir -p {new_path}")

    extract = run(f"tar -xvzf /tmp/{darchive} -C {new_path}")
    if extract.succeeded:
        run(f"rm /tmp/{darchive}")
    else:
        return False

    run("rm -rf /data/web_static/current")
    run(f"ln -s {new_path} /data/web_static/current")

    print("New version deployed!")
    return True
