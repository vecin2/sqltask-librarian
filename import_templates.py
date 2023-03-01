# This script takes a the parent folder of a templates and test_templates and imports them all into this project


# walk templates folder from source and adds each element into templates folder child

import argparse
import os
import shutil
from pathlib import Path


class Importer(object):
    def __init__(self, src, dst):
        self.src = src
        self.dst = dst

    def run(self):
        # copy each file into the templates folder
        print(f"Importing templates from {self.src}")
        self.import_folder("templates")
        self.import_folder("test_templates", exclude_list=[".tmp"])

    def import_folder(self, subfolder_name, exclude_list=[]):
        exclude_set = set(exclude_list)
        for root, dirs, files in os.walk(Path(self.src) / subfolder_name):
            # it removes subdirs inline so they are not processed by walk
            dirs[:] = [d for d in dirs if d not in exclude_set]

            dst_dir = self.dst / Path(root).relative_to(self.src)
            dst_dir.mkdir(parents=True, exist_ok=True)
            for filename in files:
                self.import_file(root, filename, dst_dir)

    def import_file(self, root, filename, dst_dir):
        srcfile = Path(os.path.join(root, filename))
        dstfile = Path(os.path.join(dst_dir, filename))
        print(f"Importing '{srcfile}' to '{dstfile}'")
        shutil.copyfile(srcfile, dstfile)


parser = argparse.ArgumentParser()
parser.add_argument("--src")
parser.add_argument("--dst")
args = parser.parse_args()

if not args.dst:
    print(
        "usage: python import_templates.py --src $EM_CORE_HOME/project/sqltask --dst prj_config/"
    )
    print(
        "usage (takes src=EM_CORE_HOME/project/sqltask):"
        "python import_templates.py --dst prj_config/"
    )
else:
    if not args.src:
        src = Path(os.getenv("EM_CORE_HOME")) / "project" / "sqltask"
    else:
        src = Path(args.src)
    Importer(src, Path(args.dst)).run()
