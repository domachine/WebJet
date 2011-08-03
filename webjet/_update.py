from os.path import getmtime, exists
from datetime import datetime

def update_file(deps, target, cb, *params):
    """
    Calls the callback ``cb'' if one of the
    dependency-files is newer than the target file.
    """

    update = False
    if not exists(target):
        cb(deps, target, *params)
    else:
        target_mtime = datetime.fromtimestamp(getmtime(target))

        for i in deps:
            if target_mtime < datetime.fromtimestamp(getmtime(i)):
                cb(deps, target, *params)
