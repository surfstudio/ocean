from distutils.dir_util import copy_tree
from glob import glob
from jinja2 import Template

import janus
import mlflow
import os


def to_camel(s):
    return ''.join(x.capitalize() or '_' for x in s.split())

def create_new_experiment(s: str):
    exps = sorted(glob('../experiments/*'))
    if len(exps) == 0:
        number = 1
    else:
        number = max([int(x.split('-')[1]) for x in exps]) + 1
    number_string = '0'*(3-len(str(number))) + str(number)
    camel_s = to_camel(s)
    exp_folder_name = 'exp-{{expNumber}}-{{expName}}'

    from_path = os.path.abspath(exp_folder_name)

    t = Template(exp_folder_name).render(expNumber=number_string, expName=s)
    to_path = os.path.join(os.path.join(os.path.dirname(os.path.dirname(from_path)), 'experiments'), t)

    copy_tree(from_path, to_path);

    exp_id = mlflow.create_experiment(name=camel_s)

    log_path = os.path.join(to_path, 'log.md')
    with open(log_path) as f:
        text = f.read()
    text_rendered = Template(text).render(expNumber=number, expName=s, expId=exp_id)
    with open(log_path, 'w') as f:
        f.write(text_rendered)

    train_path = os.path.join(to_path, 'scripts/train.py')
    with open(train_path) as f:
        text = f.read()
    text_rendered = Template(text).render(expId=exp_id)
    with open(train_path, 'w') as f:
        f.write(text_rendered)


if __name__ == '__main__':
    p = janus.ArgParser()
    p.new_str('n name')
    p.parse()
    create_new_experiment(p['name'])
