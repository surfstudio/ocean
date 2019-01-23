from jinja2 import Template
from glob import glob
from distutils.dir_util import copy_tree

import os
import re


def _render_file_inplace(path, replace_dict):
    with open(path) as f:
        template = Template(f.read())
    s = template.render(**replace_dict)
    with open(path, 'w') as f:
        f.write(s)

def create_ml_project(name, short_name, author, description,
                      version, licence, path):
    # 1. Copying template itself and renaming the root
    from_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            '{{projectNameShort}}')
    to_dir = os.path.join(path, short_name)
    copy_tree(from_dir, to_dir)

    # 2. Readme
    _render_file_inplace(path=os.path.join(to_dir, 'README.md'),
                         replace_dict={
                            'projectName': name,
                            'author': author,
                            'projectDescription': description
                         })

    # 3. Setup
    _render_file_inplace(path=os.path.join(to_dir, 'setup.py'),
                         replace_dict={
                            'projectNameShort': short_name,
                            'version': version,
                            'projectDescriptionShort': description,
                            'author': author,
                            'licence': licence
                         })

    # 4. Source folder
    src_dir_from = os.path.join(to_dir, '{{projectNameShort}}')
    src_dir_to = os.path.join(to_dir, short_name)
    os.rename(src_dir_from, src_dir_to)


def create_dl_project(name, short_name, author, description,
                      version, licence, path):
    print('Creating DL project will be implemented in the future versions')
