from generator import create_ml_project, create_dl_project

import janus
import os


def parse():
    commands_dict = {
        'new_ml': create_ml_project,
        'new_dl': create_dl_project
    }

    p = janus.ArgParser()
    p.new_str('n name')
    p.new_str('v version', fallback='0.0.1')
    p.new_str('a author', fallback='Surf')
    p.new_str('l licence', fallback='MIT')
    p.new_str('d description', fallback='')
    p.new_str('p path', fallback='.')
    p.parse()

    commands = p.get_args()
    assert len(commands) == 1, ('Please provide exactly one command. '
                           'The available commands are "new_ml" and "new_dl".')

    command = commands[0]
    assert command in commands_dict, ('The available commands are '
                                      '"new_ml" and "new_dl".')

    name = p['name']
    version = p['version']
    author = p['author']
    licence = p['licence']
    description = p['description']
    path = os.path.abspath(p['path'])

    assert len(name.strip()) > 0, 'Please provide a correct name for a project'

    short_name = ''.join([x.capitalize() for x in name.split()])
    short_name = short_name[0].lower() + short_name[1:]

    params = dict(name=name, short_name=short_name, author=author,
                  description=description, version=version, licence=licence,
                  path=path)
    commands_dict[command](**params)
