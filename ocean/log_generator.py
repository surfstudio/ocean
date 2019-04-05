from bs4 import BeautifulSoup
from datetime import datetime
from glob import glob
from jinja2 import Template

import bs4
import json
import mistune
import os
import re
import shutil
import sys


HINTS = {
    'Raw': 'Raw data provided by the customer',
    'External': 'Data taken from the Internet like weather or maps',
    'Interim': 'Intermediate data respresentation: filtered and cleaned',
    'Features': 'Features to merge with: calculated statistics and other',
    'Processed': 'Data ready to be put into models'
}

def parse_md(path):
    try:
       return BeautifulSoup(mistune.Markdown()(open(path).read()), 'lxml')
    except:
        return BeautifulSoup(mistune.Markdown()(open(path).read()), 'html.parser')

def extract_text(t):
    '''preserves <code></code> in the text'''
    if type(t) == str:
        return t
    return ''.join([str(x) for x in t.contents])

def make_re_checker(pattern):
    def has_re(s, flags=re.I):
        return len(re.findall(pattern, s, re.I)) > 0
    return has_re

def get_tags_in_between(tag_a, tag_b):
    tags = []
    for tag in tag_a.next_siblings:
        if tag == tag_b:
            break
        else:
            tags.append(tag)
    return [x for x in tags if type(x) != bs4.element.NavigableString]

def create_experiment(md):
    exp = {}
    exp['exp_name'] = extract_text(md.select_one('h1'))
    exp['task'] = extract_text(md.find('h2', text='Task').find_next('p'))
    exp['author'] = extract_text(md.find('h2', text='Author').find_next('p'))

    h3_data_generated = md.find('h3', text='Data generated')
    h3_data_taken = md.find('h3', text='Data taken')
    h2_logs = md.find('h2', text='Log')
    
    tags_data_taken = get_tags_in_between(h3_data_taken, h3_data_generated)
    tags_data_generated = get_tags_in_between(h3_data_generated, h2_logs)
    
    # data generated
    exp['data_generated'] = []
    
    rows = None
    for t in tags_data_generated:
        if t.name != 'table':
            continue
        rows = t.select_one('tbody').select('tr')

    if rows is not None:
        for row in rows:
            try:
                path, comment = row.select('td')
                clear_path = extract_text(path).strip()
                if clear_path == '':
                    continue
                exp['data_generated'].append({
                    'path': extract_text(clear_path),
                    'comment': extract_text(comment)
                })
            except ValueError:
                continue
    
    # data taken
    
    exp['data_taken'] = []
    rows = []
    for t in tags_data_taken:
        if t.name != 'ul':
            continue
        rows = t.select('li')
    exp['data_taken'] = [x.text for x in rows]
    
    # log
    
    exp['log'] = []
    
    records = []
    last_record = None
    dt_pattern = r'^(\d+\.\d+\.\d+,?\s*\d+\:\d+)'
    has_datetime = make_re_checker(dt_pattern)

    for t in h2_logs.next_siblings:
        if type(t) == bs4.element.NavigableString:
            continue
        s = extract_text(t)
        if has_datetime(s):
            if last_record is not None:
                records.append(last_record)
            last_record = [t]
        else:
            last_record.append(t)

    if len(last_record) > 0:
        records.append(last_record)
    
    log = []
    for r in records:
        s = extract_text(r[0])
        d = re.findall(dt_pattern, s)[0]
        if hasattr(r[0], 'text'):
            r[0].string = re.sub(dt_pattern+'\s+', '', r[0].text)
        ts = to_dt(d)
        s = '\n'.join([str(x) for x in r])
        item = {'datetime': ts, 'text': s}
        log.append(item)
        
    exp['log'] = log
    
    return exp

def to_dt(s):
    for p in ['%d.%m.%y, %H:%M',
              '%d.%m.%y %H:%M',
              '%d.%m.%Y, %H:%M',
              '%d.%m.%Y %H:%M']:
        try:
            return datetime.strptime(s, p).timestamp()
        except:
            continue
    print('Datetime format {0} is not understood'.format(s))
    return datetime.now().timestamp()

def fill_experiments(total, exps):
    for exp in exps:
        item = {
            'title': exp['exp_name'],
            'task': exp['task'],
            'log': []
        }
        for record in exp['log']:
            item['log'].append({
                'datetime': record['datetime'],
                'text': record['text'],
                'author': exp['author']
            })
        total['experiments'].append(item)

def fill_history(total, exps):
    records = []
    for exp in exps:
        for record in exp['log']:
            item = {
                'datetime': record['datetime'],
                'text': record['text'],
                'exp': 'Exp. {}'.format(re.findall(r'Experiment (\d+)', exp['exp_name'])[0]),
                'author': exp['author']
            }
            records.append(item)
    total['history'] = sorted(records, key=lambda d: to_dt(d['datetime']))

def fill_data(total, exps):
    for e in exps:
        full_exp_name = e['exp_name'][len('Experiment '):]
        exp_name = 'Exp. {}'.format(re.findall(r'Experiment (\d+)', e['exp_name'])[0])

        for p in e['data_generated']:
            item = {
                'comment': p['comment'],
                'filename': p['path'].split('/')[-1],
                'created_in': exp_name,
                'used_in': [exp_name]
            }
            path = p['path']
            if path.startswith('/'):
                path = path[1:]
            ps = path.split('/')
            if path.startswith('experiments/exp-'):
                models = total['data']['models']
                if full_exp_name in models:
                    models[full_exp_name].append(item)
                else:
                    models[full_exp_name] = [item]
            else:
                data = total['data']['data']
                key = ps[1]
                if key in data:
                    data[key].append(item)
                else:
                    data[key] = [item]

        for p in e['data_taken']:
            if p.startswith('/'):
                p = p[1:]
            ps = p.split('/')
            main_key = ps[0]
            key = ps[1]
            filename = ps[-1]
            d = total['data'][main_key]
            if key not in d:
                d[key] = [{
                    'comment': '-',
                    'filename': filename,
                    'created_in': '<i>Unknown</i>',
                    'used_in': [exp_name]
                }]
            else:
                found = False
                for rec in d[key]:
                    if rec['filename'] == filename:
                        found = True
                        rec['used_in'].append(exp_name)
                        rec['used_in'] = sorted(set(rec['used_in']))
                if not found:
                    d[key].append({
                        'comment': '-',
                        'filename': filename,
                        'created_in': '<i>Unknown</i>',
                        'used_in': [exp_name]
                    })

def generate_html_notebooks(md, np, html_path):
    cmd = 'jupyter nbconvert {0} --output {1}'
    for p in md.find('h2', text='Log').find_next_siblings('p'):
        for a in p.find_all('a'):
            if ('href' in a.attrs) and \
               len(re.findall(r'notebooks/.*\.ipynb', a.attrs['href'])) > 0:

                    href = a.attrs['href']
                    name = href.split('/')[-1]
                    if name.endswith('.ipynb'):
                        name_html = name[:len(name)-len('.ipynb')] + '.html'
                    dest_path = os.path.join(html_path, name_html)

                    c = cmd.format(np + '/'+ href, dest_path)
                    os.system(c)

                    s = '/'.join(['html', name.replace('ipynb', 'html')])
                    a.attrs['href'] = s

def generate_log(root_folder):
    package_folder = os.path.dirname(os.path.abspath(__file__))
    template_folder = os.path.join(package_folder, 'project_log')
    print(template_folder)
    
    log_folder = os.path.join(root_folder, 'project_log')
    html_path = os.path.join(log_folder, 'project_log.html')
    html_log_folder = os.path.join(log_folder, 'html')
    
    exp_folder = os.path.join(root_folder, 'experiments')
    readme_path = os.path.join(root_folder, 'README.md')

    if os.path.exists(log_folder):
        shutil.rmtree(log_folder)

    total = {
        'experiments': [],
        'history': [],
        'data': {
            'data': {},
            'models': {}
        },
        'hints': HINTS
    }

    ps = sorted(glob(os.path.join(exp_folder, '*/*.md')))
    if len(ps) == 0:
        print('No logs were found')
    else:
        shutil.copytree(template_folder, log_folder)

        mds = [parse_md(p) for p in ps]
        nps = [os.path.dirname(p) for p  in ps]

        for md, np in zip(mds, nps):
            generate_html_notebooks(md, np, html_log_folder)

        exps = [create_experiment(md) for md in mds]

        fill_experiments(total, exps)
        fill_history(total, exps)
        fill_data(total, exps)

        tree = parse_md(readme_path)
        project_name = tree.select_one('h1').text

        s = json.dumps(total, indent=2)
        s = Template(open(html_path).read()).render(json=s,
                                                    projectName=project_name)
        with open(html_path, 'w') as f:
            f.write(s)
