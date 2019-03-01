from bs4 import BeautifulSoup
from distutils.dir_util import copy_tree
from .docs_index_generator import make_doc_index
from .log_generator import parse_md
from jinja2 import Template
from glob import glob

import janus
import mistune
import os
import re
import sys
import shutil


def parse():
    parser = janus.ArgParser()

    #  ===== PROJECT ===== 
    project_parser = parser.new_cmd('project', 
                                    'Project command', 
                                     project_command)

    new_project_parser = project_parser.new_cmd('new', 
                                                'Creates new project', 
                                                 project_new_command)
    new_project_parser.new_str('n name')
    new_project_parser.new_str('v version', fallback='0.0.1')
    new_project_parser.new_str('a author', fallback='Surf')
    new_project_parser.new_str('l licence', fallback='MIT')
    new_project_parser.new_str('d description', fallback='')
    new_project_parser.new_str('p path', fallback='.')

    #  ===== EXPERIMENT ===== 
    experiment_parser = parser.new_cmd('exp', 
                                       'Experiment command', 
                                        experiment_command)

    new_exp_parser = experiment_parser.new_cmd('new', 
                                               'Creates new experiment', 
                                                new_experiment_command)
    new_exp_parser.new_str('n name')
    new_exp_parser.new_str('a author')
    new_exp_parser.new_str('t task', fallback='')
    new_exp_parser.new_str('p path', fallback='.')

    # TODO:
    list_exp_parser = experiment_parser.new_cmd('list', 
                                                'List all experiments', 
                                                 list_experiments_command)
    list_exp_parser.new_str('p path', fallback='.')
    list_exp_parser.new_flag('a author')
    list_exp_parser.new_flag('t task')

    #  ===== ENVIRONMENTS ===== 
    env_parser = parser.new_cmd('env', 
                                'Environment command', 
                                env_command)

    new_env_parser = env_parser.new_cmd('new', 
                                        'Creates new environment', 
                                        create_env_command)
    new_env_parser.new_str('n name', fallback='')
    new_env_parser.new_str('p path', fallback='.')
    
    show_env_parser = env_parser.new_cmd('show', 
                                         'Shows kernels environment', 
                                         show_env_command)

    delete_env_parser = env_parser.new_cmd('delete', 
                                         'Delete current environment', 
                                         delete_env_command)
    delete_env_parser.new_str('n name', fallback='')
    delete_env_parser.new_str('p path', fallback='.')
    
    #  ===== LOG ===== 
    # TODO:
    log_parser = parser.new_cmd('log', 
                                'Log command', 
                                 log_command)

    # TODO:
    new_log_parser = log_parser.new_cmd('new', 
                                        'Creates new project log', 
                                         create_log_command)

    # TODO:
    new_log_parser = log_parser.new_cmd('archive', 
                                        'Archives log', 
                                         arch_log_command)
    parser.parse()

    #  ===== DOC ===== 
    doc_parser = parser.new_cmd('docs', 
                                'Docs command', 
                                 doc_command)

# ===================================================================== 

def project_command(p):
    if p.has_cmd():
        return
    print('PROJECT COMMAND HELP')
    print('Usage:')
    print(' > ocean project new ...')
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
    print(' > ocean exp new ... - Creates new experiment')
    print('       -n --name   : Experiment name like "Boosting". Must be provided.')
    print('       -a --author : Author. Must be provided')
    print(('       -t --task   : Task of an experiment. Default: "", so '
           'the one can specify it later on.'))
    print(('       -p --path   : Path to the root folder, default is . (current folder). '
                'Ocean performs search of an root folder automatically, so '
                'you can perform this command in any nested folder.'
               ))
    print(' > ocean exp list - List all experiments')

def new_experiment_command(p):
    name = p['name']
    author = p['author']
    if name is None:
        print(('Experiment name must be provided. '
               'Use "ocean exp new -n EXP_NAME -a AUTHOR" syntax'), 
              file=sys.stderr)
        return
    if author is None:
        print(('Author name must be provided. Use "ocean exp new '
               '-n EXP_NAME -a AUTHOR" syntax'), 
              file=sys.stderr)
        return
    task = p['task']
    if task == '':
        task = 'Describe your task here.'
    path = os.path.abspath(p['path'])
    camel_name = _to_camel(name)

    found, root = _find_ocean_root(path)
    if not found:
        print('Please specify project path via -p argument', file=sys.stderr)
        return
    exps = os.path.join(root, 'experiments')
    project_name = root.split('/')[-1]

    exps_created = sorted(glob(os.path.join(exps, '*')))

    used_names = [x.split('-', 2)[-1] for x in exps_created]
    if name is used_names:
        print('Experiment name must be unique!', file=sys.stderr)
        return

    if len(exps_created) == 0:
        number = 1
    else:
        number = max([int(x.split('-')[1]) for x in exps_created]) + 1
    number_string = '0'*(3-len(str(number))) + str(number)
    exp_folder_name = 'exp-{0}-{1}'.format(number_string, camel_name)

    from_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                             'exp-{{expNumber}}-{{expName}}')                             
    to_path = os.path.join(exps, exp_folder_name)
    copy_tree(from_path, to_path)

    log_path = os.path.join(to_path, 'log.md')
    with open(log_path) as f:
        text = f.read()
    text_rendered = Template(text).render(expNumber=number, 
                                          expName=name,
                                          author=author,
                                          task=task)
    with open(log_path, 'w') as f:
        f.write(text_rendered)

    train_path = os.path.join(to_path, 'scripts/train.py')
    with open(train_path) as f:
        text = f.read()
    text_rendered = Template(text).render(projectNameShort=project_name)
    with open(train_path, 'w') as f:
        f.write(text_rendered)

def list_experiments_command(p):
    path = p['path']
    show_authors = p['author']
    show_tasks = p['task']
    found, root = _find_ocean_root(path)
    if not found:
        print('Please specify project path via -p argument', file=sys.stderr)
        return
    exps = os.path.join(root, 'experiments')
    if not os.path.exists(exps):
        print('Haven\'t found the experiments folder in project\'s root', 
            file=sys.stderr)
        return
    exps = sorted(glob(os.path.join(exps, '*')))
    results = []
    for exp_folder in exps:
        results.append(_parse_experiment(exp_folder, show_authors, show_tasks))
    for item in results:
        print(item['exp_name'])
        if show_authors:
            print('\tAuthor: {}'.format(item['author']))
        if show_tasks:
            print('\tTask: {}'.format(item['task']))
        if show_authors or show_tasks:
            print()

def _parse_experiment(folder, show_authors, show_tasks):
    md_path = os.path.join(folder, 'log.md')
    md = parse_md(md_path)
    result = {}
    result['exp_name'] = md.select_one('h1').text
    if show_authors:
        result['author'] = md.find('h2', text='Author').find_next('p').text
    if show_tasks:
        result['task'] = md.find('h2', text='Task').find_next('p').text
    return result

def env_command(p):
    if p.has_cmd():
        return
    print('ENVIRONMENT COMMAND HELP')
    print('Usage:')
    print(' > ocean env new ... - Creates new venv and relative Jupyter kernel for the experiment')
    print(('       -n --name   : Environment name like "Doggie". '
           'If not specified, experiment folder\'s name will be taken.'))
    print(('       -p --path   : Path to the experiment folder, default is . (current folder). '
                'Ocean performs search of an experiment\'s root folder automatically, so '
                'you can perform this command in any nested folder.'
               ))
    print(' > ocean env show - Shows list of all environments.')
    print((' > ocean env delete - Delete current environment. '
           'Additional parameters are same with `new` command'))

def create_env_command(p):
    name = p['name']
    path = p['path']
    exp_root = _find_experiment_root(path)
    _create_kernel(exp_root, name)

def show_env_command(p):
    cmd = 'jupyter kernelspec list'
    os.system(cmd)

def delete_env_command(p):
    name = p['name']
    path = p['path']
    exp_root = _find_experiment_root(path)
    _remove_kernel(exp_root, name)

def doc_command(p):
    print('DOCS')

def log_command(p):
    if p.has_cmd():
        return
    print('LOG COMMAND HELP')
    print('Usage:')
    print(' > ocean log new - Creates project log')
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
    new_config = []
    project_name = None
    to_find = ['import os', 'import sys', 'sys.path.insert']
    to_append = ['import os\n', 'import sys\n', 'sys.path.insert(0, "..")\n']
    with open(os.path.join(docs_dir, 'conf.py')) as f:
        config = f.readlines()
        for line in config:
            found = False
            for i in range(len(to_find)):
                if to_find[i] in line:
                    found = True
                    new_config.append(to_append[i])
                    break
            if not found:
                new_config.append(line)
            capts = re.findall(r'project\s+\=\s+\'(.+)\'', line, flags=re.I)
            if len(capts) > 0:
                project_name = capts[0]
    new_config.append('autodoc_mock_imports = ["yaml", "numpy", "pandas"]\n')
    new_config.append(('exclude_patterns = '
                       '["setup.rst", "{0}.rst", "{0}.data.rst"]\n').format(project_name))
    with open(os.path.join(docs_dir, 'conf.py'), 'w') as f:
        f.write(''.join(new_config))

def _generate_docs(root):
    docs = os.path.join(root, 'docs')
    index_rst = os.path.join(docs, 'index.rst')
    make_doc_index(root_path=root, doc_index_path=index_rst)
    cmd = 'cd {} && make html >/dev/null'.format(docs)
    os.system(cmd)

def _install_as_package(root):
    command = 'cd {0}; make -B package >/dev/null'.format(root)
    os.system(command)

def _create_kernel(f, name=''):
    full_foldername = os.path.abspath(f)
    folder = full_foldername.split('/')[-1]
    name = folder if name == '' else name
    cmd = ('cd {0} && '
           'python3 -m venv env && '
           'source env/bin/activate && '
           'pip install ipykernel && '
           'python -m ipykernel install --user --name "{1}" --display-name "Python ({1})" && '
           'pip install -r requirements.txt && '
           'deactivate'
           ).format(full_foldername, name)
    os.system(cmd)

def _remove_kernel(f, name=''):
    full_foldername = os.path.abspath(f)
    folder = full_foldername.split('/')[-1]
    name = folder if name == '' else name
    s = (
        'jupyter kernelspec uninstall "{0}" -f && '
        'rm -rf env'
    ).format(name)
    os.system(s)

# =============================================================================

def _capitalizeOne(s):
    return s[0].upper() + s[1:]

def _render_file_inplace(path, replace_dict):
    with open(path) as f:
        template = Template(f.read())
    s = template.render(**replace_dict)
    with open(path, 'w') as f:
        f.write(s)

def _find_ocean_root(path):
    return _find_root(path, '.ocean')

def _find_experiment_root(path):
    return _find_root(path, '.exp')

def _find_root(path, hidden):
    root = None
    found = False
    old_f = os.path.abspath(path)
    f = os.path.dirname(old_f)
    while f != old_f:
        hidden_path = os.path.join(old_f, hidden)
        if os.path.exists(hidden_path):
            found = True
            root = old_f
            break
        old_f = f
        f = os.path.dirname(f)
    return found, root

def _to_camel(s):
    return ''.join(x[0].upper()+x[1:] for x in s.split())

# =============================================================================

if __name__ == '__main__':
    parse()
