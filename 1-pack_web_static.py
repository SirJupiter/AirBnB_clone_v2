#!/usr/bin/python3
"""Fabric script that generates a .tgz archive
from the contents of the web_static folder of your AirBnB Clone repo,
using the function do_pack
"""

from datetime import datetime
import fabric.api import local


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
    darchive = f"web_static_{year}{month}{day}{hour}{minute}{sec}.tgz"

    local('mkdir -p versions')
    created = local(f'tar -cvzf versions/{darchive} web_static')

    if created.failed:
        return None

    return darchive
