from .persistence import load, save

import glob
import json
import os
import re
import yaml
import pandas as pd


class Path:
    """
    **Incapsulates directory surfing**

    - Example::

        p = Path('.')
        p

        > '/opt/shared/kishenya'

        p.join('data').join('raw')

        > '/opt/shared/kishenya/data/raw'

        p.join('data').join('raw').back()
        p.join('data').join('raw').up()  # same

        > '/opt/shared/kishenya/data'

        p.join('data').exists

        > True

        p.join('dataakjnfjknajkn').exists

        > False

        p.join('data').join('raw').contents()

        > ['/opt/shared/kishenya/data/raw/cards_ai.csv',
           '/opt/shared/kishenya/data/raw/retail_ai.csv',
           '/opt/shared/kishenya/data/raw/shop_ai.csv']

        p.save([1,2,3])

        > None

        p.load()

        > [1,2,3]
    """
    def __init__(self, s: str):
        self.path = os.path.abspath(s)

    def __repr__(self):
        return self.path

    def join(self, other):
        return Path(os.path.join(self.path, other))

    def back(self):
        return Path(os.path.dirname(self.path))

    def up(self):
        return self.back()

    def load(self, *args, **kwargs):
        if self.path.endswith('yml') or self.path.endswith('yaml'):
            return yaml.load(open(self.path)) 
        if self.path.endswith('csv'):
            return pd.read_csv(self.path, *args, **kwargs)
        if self.path.endswith('json'):
            return json.load(open(self.path))
        # treat as pickle object
        return load(self.path)

    def save(self, obj):
        save(obj, self.path)

    def contents(self, recursive: bool = True):
        if recursive:
            p = glob.glob(os.path.join(self.path, '**'), recursive=True)
        else:
            p = glob.glob(os.path.join(self.path, '*'), recursive=False)
        return sorted([x for x in p if not os.path.isdir(x)], key=lambda s: s.lower())

    @property
    def exists(self):
        return os.path.isdir(self.path) or os.path.isfile(self.path)

class Coordinator:
    """
    **Provides paths to main folders**

    Initializes paths to `root`, `src`, ...

    .. note:: Every field is a member of Path, not str!

    - Example::

        # From a notebook
        c = Coordinator()

        c.root

        > '/opt/shared/kishenya'

        c.data_interim

        > '/opt/shared/kishenya/data/interim'
    """
    def __init__(self, path: str='.'):
        p = os.path.abspath(path)
        while not os.path.exists(os.path.join(p, '.ocean')):
            p = os.path.dirname(p)
        self.root = Path(p)
        self.config = self.root.join('config')
        self.data = self.root.join('data')
        self.data_raw = self.data.join('raw')
        self.data_interim = self.data.join('interim')
        self.data_external = self.data.join('external')
        self.data_features = self.data.join('features')
        self.data_processed = self.data.join('processed')
        self.demos = self.root.join('demos')
        self.docs = self.root.join('docs')
        self.notebooks = self.root.join('notebooks')
        self.references = self.root.join('references')

    # Hooks
    @property
    def alarm_config(self):
        return self.config.join('alarm_config.yml').load()
    
    @property
    def logging_config(self):
        return self.config.join('logging_config.yml').load()


class ExperimentCoordinator:
    def __init__(self, path='.'):
        p = os.path.abspath(path)
        while len(re.findall(r'exp\-\d+', p.split('/')[-1])) == 0:
            p = os.path.dirname(p)
        self.root = Path(p)
        self.config = self.root.join('config')
        self.mlruns = self.root.join('mlruns')
        self.models = self.root.join('models')
        self.notebooks = self.root.join('notebooks') 
        self.references = self.root.join('references') 
        self.scripts = self.root.join('scripts')     
        self.utils = self.root.join('utils')
    
    @property
    def base_coordinator(self):
        return Coordinator(self.root.back().back().path)
    
    # Hooks
    @property
    def alarm_config(self):
        c = self.base_coordinator
        return c.config.join('alarm_config.yml').load()
    
    @property
    def logging_config(self):
        c = self.base_coordinator
        return c.config.join('logging_config.yml').load()
