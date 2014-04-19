import time
import os
import tarfile
from collections import namedtuple

BackupStruct = namedtuple('BackupStruct', ["src", "tgt"])

def backup_posts(args, logger):
    """
    Makes a tarfile out of the src dir and saves it into the target.
    Meant to be used for backing-up posts directory
    """
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    tgt_file_name = timestamp + '.tar.gz'
    tgt_file = os.path.join(args.tgt, tgt_file_name)

    with tarfile.open(tgt_file, "w:gz") as tar:
        arcname = os.path.basename(args.src) + '-' + timestamp
        tar.add(args.src, arcname=arcname)

    logger.info("Posts successfully backed up. Create tar file at {}".format(tgt_file))

def make_backup(src, tgt, logger):
    " Wrapper for backup_posts command "
    backup_args = BackupStruct(src=src, tgt=tgt)
    backup_posts(backup_args, logger)
