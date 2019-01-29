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
    
    os.system('cd {0} && sudo python3 filler.py -f {1} -c {2} -n {3}'.format(to_path, s, camel_s, number))
    

if __name__ == '__main__':
    p = janus.ArgParser()
    p.new_str('n name')
    p.parse()
    create_new_experiment(p['name'])
