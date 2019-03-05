from jinja2 import Template
from toolz import groupby

import glob
import janus
import os
import re


def make_doc_index(root_path: str, doc_index_path: str):
    d = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'docs')
    template = os.path.join(d, 'docsIndexTemplate.jinja')
    with open(template) as f:
        template = Template(f.read())

    project_name = root_path.split('/')[-1]
    src_folder = os.path.join(root_path, project_name)
    if not root_path.endswith('/'):
        root_path = root_path + '/'
    fs = [x.replace(root_path, '') 
          for x in glob.glob('{}/**'.format(src_folder), recursive=True)
          if ('__pycache__' not in x) and ('__init__' not in x)]

    fs = [x for x in fs if not os.path.isdir(x)]
    fg = groupby(key=lambda s: os.path.dirname(s), seq=fs)
    
    S = ''
    for k in sorted(fg.keys()):
        s = 'Module {}'.format(k)
        S += s + '\n'
        S += '='*len(s) + '\n\n'

        for x in sorted(fg[k]):
            q = x[:-3].replace('/', '.')  # -3 is for ".py"
            t = ' '.join(q.split('.')[-1].split('_')).capitalize()

            S += t + '\n'
            S += '*'*len(t) + '\n'
            S += '.. automodule:: {}'.format(q) + '\n'
            S += '   :members:\n'
            S += '   :undoc-members:\n'
            S += '   :show-inheritance:\n'
            S += '   :noindex:\n\n'

    rendered_project_name = '{0}\n{1}'.format(project_name, '='*len(project_name))
    S = template.render(project_name=rendered_project_name, refs=S)
    with open(doc_index_path, 'w') as f:
        f.write(S)