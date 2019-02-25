from jinja2 import Template

import janus
import os
import sys
import subprocess


def fill(fullname, camelcase_name, number, project_name):
    folder = os.path.dirname(os.path.abspath(__file__))
    
    log_path = os.path.join(folder, 'log.md')
    with open(log_path) as f:
        text = f.read()
    text_rendered = Template(text).render(expNumber=number, expName=fullname)
    with open(log_path, 'w') as f:
        f.write(text_rendered)

    train_path = os.path.join(folder, 'scripts/train.py')
    with open(train_path) as f:
        text = f.read()
    text_rendered = Template(text).render(projectNameShort=project_name)
    with open(train_path, 'w') as f:
        f.write(text_rendered)
    
    # self-destruct
    os.remove(os.path.join(folder, sys.argv[0]))


if __name__ == '__main__':
    p = janus.ArgParser()
    p.new_str('f fullname')
    p.new_str('c camel')
    p.new_int('n number')
    p.new_str('p proj_name')
    p.parse()
    fill(fullname=p['f'], camelcase_name=p['c'], number=p['n'], project_name=p['p'])
