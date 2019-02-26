from distutils.dir_util import copy_tree
from .docs_index_generator import make_doc_index
from jinja2 import Template
from glob import glob

import janus
import os
import re
import shutil


def parse():
    parser = janus.ArgParser()

    project_parser = parser.new_cmd('project', 
                                    'Project command', 
                                     project_command)

    new_project_parser = project_parser.new_cmd('create', 
                                                'Creates new project', 
                                                 project_new_command)
    new_project_parser.new_str('n name')
    new_project_parser.new_str('v version', fallback='0.0.1')
    new_project_parser.new_str('a author', fallback='Surf')
    new_project_parser.new_str('l licence', fallback='MIT')
    new_project_parser.new_str('d description', fallback='')
    new_project_parser.new_str('p path', fallback='.')

    experiment_parser = parser.new_cmd('exp', 
                                       'Experiment command', 
                                        experiment_command)

    new_exp_parser = experiment_parser.new_cmd('create', 
                                               'Creates new experiment', 
                                                new_experiment_command)
    new_exp_parser.new_str('n name')
    new_exp_parser.new_str('a author')
    new_exp_parser.new_str('t task', fallback='')

    list_exp_parser = experiment_parser.new_cmd('list', 
                                                'List all experiments', 
                                                 new_experiment_command)
    
    log_parser = parser.new_cmd('log', 
                                'Log command', 
                                 log_command)

    new_log_parser = log_parser.new_cmd('create', 
                                        'Creates new project log', 
                                         create_log_command)

    new_log_parser = log_parser.new_cmd('archive', 
                                        'Archives log', 
                                         arch_log_command)
    parser.parse()

# ===================================================================== 

def project_command(p):
    if p.has_cmd():
        return
    print('PROJECT COMMAND HELP')
    print('Usage:')
    print(' > ocean project create ...')
    print('       -n --name        : Project name like "Cute kittens". Must be provided.')
    print('       -v --version     : Version. Default: "0.0.1".')
    print('       -a --author      : Author. Default: "Surf".')
    print('       -l --licence     : License. Default: "MIT".')
    print('       -d --description : Description. Default: "".')
    print('       -p --path        : Path. Default: ".", which is the current directory.')

def project_new_command(p):
    name = p['name']
    version = p['version']
    author = p['author']
    licence = p['licence']
    description = p['description']
    path = os.path.abspath(p['path'])

    short_name = ''.join([_capitalizeOne(w) for w in name.split()])
    short_name = short_name[0].lower() + short_name[1:]

    create_project(name=name, short_name=short_name, author=author,
                   description=description, version=version, licence=licence,
                   path=path)

def experiment_command(p):
    if p.has_cmd():
        return
    print('EXPERIMENT COMMAND HELP')
    print('Usage:')
    print(' > ocean exp create ... - Creates new experiment')
    print('       -n --name   : Experiment name like "Boosting". Must be provided.')
    print('       -a --author : Author. Must be provided')
    print(('       -t --task   : Task of an experiment. Default: "", so '
           'the one can specify it later on.'))
    print(' > ocean exp list - List all experiments')
    
def new_experiment_command(p):
    print('EXPERIMENT NEW')

def list_experiment_command(p):
    print('EXPERIMENT LIST')

def log_command(p):
    if p.has_cmd():
        return
    print('LOG COMMAND HELP')
    print('Usage:')
    print(' > ocean log create - Creates project log')
    print(' > ocean log archive ... - Archives existing project log')
    print('       -n --name     : Name of the archive like "result". Must be provided.')
    print('       -p --password : Password. Default is "" - no password.')

def create_log_command(p):
    print('LOG CREATE')

def arch_log_command(p):
    print('LOG ARCH')

# ===================================================================== 

def create_project(name, short_name, author, description,
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
    _generate_docs(root)
    # 8. Install project package by default
    _install_as_package(root)

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
    shutil.move(src_dir_from, src_dir_to)

def _generate_sphinx_docs(root, name, author, version):
    docs_dir = os.path.join(root, 'docs')
    command = ('cd {0} && '
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
    for i, line in enumerate(config):
        for to_uncomment in lines_to_uncomment:
            if to_uncomment in line:
                config[i] = line[2:]
        if 'sys.path.insert' in line:
            config.insert(i+1, 'sys.setrecursionlimit(1500)\n')
    with open(os.path.join(docs_dir, 'conf.py'), 'w') as f:
        f.write(''.join(config))

def _generate_docs(root):
    docs = os.path.join(root, 'docs')
    index_rst = os.path.join(docs, 'index.rst')
    make_doc_index(root_path=root, doc_index_path=index_rst)
    cmd = 'cd {} && make html >/dev/null'.format(docs)
    os.system(cmd)

def _install_as_package(root):
    command = 'cd {0}; make -B package >/dev/null'.format(root)
    os.system(command)

# =============================================================================

def _capitalizeOne(s):
    return s[0].upper() + s[1:]

def _render_file_inplace(path, replace_dict):
    with open(path) as f:
        template = Template(f.read())
    s = template.render(**replace_dict)
    with open(path, 'w') as f:
        f.write(s)

# =============================================================================

if __name__ == '__main__':
    parse()
