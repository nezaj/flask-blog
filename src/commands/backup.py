import time
import os
import tarfile

def backup_posts(args):
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
