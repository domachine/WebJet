
import sys
from os.path import dirname, abspath

import jinja2

try:
    import yaml
except ImportError:
    # TODO: Implement a fallback method to JSON.
    print('PyYAML module not found.', file=sys.stderr)
    exit(1)

from webjet._module_loader import MultiModuleLoader


__all__ = ['BaseProject', 'WebProject']


class BaseProject(object):
    def __init__(self, cfg):
        self._cfg = cfg

    def load_modules(self):
        print('Loading modules')
        modules = self._cfg['modules'] if 'modules' in self._cfg else []

        # Autoloaded core modules.
        modules = modules + ['webjet.processor']

        env_args = {'extensions': []}

        mod_loader = MultiModuleLoader()

        for mod in modules:
            cpld_mod = __import__(mod, fromlist=['DEPENDENCIES', 'PRIORITY',
                                                 'init', 'run'])
            mod_loader.add(cpld_mod)

        mod_loader.load('init', [self._cfg, env_args])
        self._env = jinja2.Environment(**env_args)
        mod_loader.load('run', [self._cfg, self._env])


class WebProject(BaseProject):
    def __init__(self, cfg_file):

        with open(cfg_file) as cfg_file_descr:
            cfg = yaml.load(cfg_file_descr)

            if 'project_dir' not in cfg:
                cfg['project_dir'] = dirname(cfg_file)

            BaseProject.__init__(self, cfg)
