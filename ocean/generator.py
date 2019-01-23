import janus


COMMANDS = ['new_ml', 'new_dl']

def main():
    p = janus.ArgParser()
    p.new_str('n name')
    p.new_str('v version', fallback='0.0.1')
    p.new_str('a author', fallback='Surf')
    p.new_str('l licence', fallback='MIT')
    p.new_str('d description', fallback='')
    p.parse()

    commands = p.get_args()
    assert len(commands) == 1, ('Please provide exactly one command. '
                           'The available commands are "new_ml" and "new_dl".')

    command = commands[0]
    assert command in COMMANDS, ('The available commands are '
                                 '"new_ml" and "new_dl".')

    name = p['name']
    version = p['version']
    author = p['author']
    licence = p['licence']
    description = p['description']

    assert len(name.strip()) > 0, 'Please provide a correct name for a project'

    short_name = ''.join([x.capitalize() for x in name.split()])
    short_name = short_name[0].lower() + short_name[1:]

    print(name, short_name, version, author, licence, description)
