import os
import platform
import portalocker
import json
import datetime
import sys

def walklevel(some_dir, level=1):
    some_dir = some_dir.rstrip(os.path.sep)
    assert os.path.isdir(some_dir)
    num_sep = some_dir.count(os.path.sep)
    for root, dirs, files in os.walk(some_dir):
        yield root, dirs, files
        num_sep_this = root.count(os.path.sep)
        if num_sep + level <= num_sep_this:
            del dirs[:]

def creation_date(path_to_file):
    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    """
    if platform.system() == 'Windows':
        return os.path.getmtime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        return stat.st_mtime

def json_safe_dump(path_to_file, contents):
    jsonFile = open(path_to_file, 'w')
    portalocker.lock(jsonFile, portalocker.LOCK_EX)
    json.dump(contents, jsonFile, indent=4)
    jsonFile.close()

def json_safe_read(path_to_file):
    contents = None

    try:
        jsonFile = open(path_to_file, 'r')
        portalocker.lock(jsonFile, portalocker.LOCK_EX)
        contents = json.load(jsonFile)       
        jsonFile.close()   
    except:
        pass

    return contents

def file_last_modified_longer_than(path_to_file, time_in_seconds):
    if os.path.exists(path_to_file) is False:
        return True

    last_modified = datetime.datetime.fromtimestamp(os.path.getmtime(path_to_file))
    now = datetime.datetime.now()

    return (now - last_modified).seconds > time_in_seconds