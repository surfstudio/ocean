from jinja2 import Template
from toolz import groupby

import glob
import janus
import os
import re


def make_doc_index(template_path: str, doc_index_path: str):
    with open(template_path) as f:
        template = Template(f.read())

    project_name = os.path.dirname(
                       os.path.dirname(os.path.abspath(__file__))
                   ).split('/')[-1]

    fs = [x for x in glob.glob('../{}/**'.format(project_name), recursive=True)
          if ('__pycache__' not in x) and ('__init__' not in x)]
    fs = [x for x in fs if not os.path.isdir(x)]
    fg = groupby(key=lambda s: os.path.dirname(s), seq=fs)

    S = ''
    for k in sorted(fg.keys()):
        s = 'Module {}'.format(k[3:])
        S += s + '\n'
        S += '='*len(s) + '\n\n'

        for x in sorted(fg[k]):

            q = x[3:-3].replace('/', '.')
            t = ' '.join(q.split('.')[-1].split('_')).capitalize()

            S += t + '\n'
            S += '*'*len(t) + '\n'
            S += '.. automodule:: {}'.format(q) + '\n'
            S += '   :members:\n'
            S += '   :noindex:\n\n'

    rendered_project_name = '{0}\n{1}'.format(project_name, '='*len(project_name))
    S = template.render(project_name=rendered_project_name, refs=S)
    with open(doc_index_path, 'w') as f:
        f.write(S)


if __name__ == '__main__':
    p = janus.ArgParser()
    p.new_str('t template')
    p.new_str('s save')
    p.parse()
    make_doc_index(p['template'], p['save'])
