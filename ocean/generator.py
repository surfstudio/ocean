from jinja2 import Template
from glob import glob
from distutils.dir_util import copy_tree

import os
import re


def create_ml_project(name, short_name, author, description,
                      version, licence, path):
    # 1. Copying template itself and renaming the root
    root = _copy_template(path, short_name)
    # 2. Readme
    _render_readme(root, name, author, description)
    # 3. Setup
    _render_setup_py(root, short_name, version, description, author, licence)
    # 4. Source folder
    _rename_src_folder(root, short_name)
    # 5. Documentation
    docs_dir = _generate_sphinx_docs(root, name, author, version)
    # 6. Documentation's configuration
    _change_sphinx_config(docs_dir)
    # 7. Generate docs
    # TODO:

def create_dl_project(name, short_name, author, description,
                      version, licence, path):
    print('Creating DL project will be implemented in the future versions')

def _render_file_inplace(path, replace_dict):
    with open(path) as f:
        template = Template(f.read())
    s = template.render(**replace_dict)
    with open(path, 'w') as f:
        f.write(s)

def _copy_template(path, short_name):
    from_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            '{{projectNameShort}}')
    to_dir = os.path.join(path, short_name)
    copy_tree(from_dir, to_dir)
    return to_dir

def _render_readme(root, name, author, description):
    _render_file_inplace(path=os.path.join(root, 'README.md'),
                         replace_dict={
                            'projectName': name,
                            'author': author,
                            'projectDescription': description
                         })

def _render_setup_py(root, short_name, version, description, author, licence):
    _render_file_inplace(path=os.path.join(root, 'setup.py'),
                         replace_dict={
                            'projectNameShort': short_name,
                            'version': version,
                            'projectDescriptionShort': description,
                            'author': author,
                            'licence': licence
                         })

def _rename_src_folder(root, short_name):
    src_dir_from = os.path.join(root, '{{projectNameShort}}')
    src_dir_to = os.path.join(root, short_name)
    os.rename(src_dir_from, src_dir_to)

def _generate_sphinx_docs(root, name, author, version):
    docs_dir = os.path.join(root, 'docs')
    command = ('cd {0}; '
               'sphinx-apidoc -o . .. -FEP -H "{1}" -A "{2}" -V "{3}" '
               '>/dev/null')\
              .format(docs_dir, name, author, version)
    os.system(command)
    return docs_dir

def _change_sphinx_config(docs_dir):
    """
    The settings changes are taken from here
    https://medium.com/@richyap13/a-simple-tutorial-on-how-to-document-your-\
        python-project-using-sphinx-and-rinohtype-177c22a15b5b
    """
    with open(os.path.join(docs_dir, 'conf.py')) as f:
        config = f.readlines()
    lines_to_uncomment = [
        'import os',
        'import sys',
        'sys.path.insert'
    ]
    latex_block_started = False
    for i, line in enumerate(config):
        for to_uncomment in lines_to_uncomment:
            if to_uncomment in line:
                config[i] = line[2:]
        if 'sys.path.insert' in line:
            config.insert(i+1, 'sys.setrecursionlimit(1500)\n')

        if len(re.findall(r'extensions\s+=\s+\[', line)) > 0:
            bracket_index = line.index('[')
            with_rinoh = line[:bracket_index + 1] + \
                         "'rinoh.frontend.sphinx', " + \
                         line[bracket_index + 1:]
            config[i] = with_rinoh

        if len(re.findall(r'latex_elements\s+=\s\{', line)) > 0:
            latex_block_started = True
        if '}' in line and latex_block_started:
            latex_block_started = False
        if latex_block_started and len(re.findall(r'\#\s+\'\w+', line)) > 0:
            config[i] = line.replace('#', '')
    with open(os.path.join(docs_dir, 'conf.py'), 'w') as f:
        f.write(''.join(config))
