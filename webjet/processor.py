from os.path import join
from datetime import datetime

import jinja2

from webjet._update import update_file


PRIORITY = 2

def init(cfg, env_cfg):
    for i in ('block_start_string',
              'block_end_string',
              'extensions'):
        if i in cfg:
            env_cfg[i] = cfg[i]

    env_cfg['loader'] = jinja2.FileSystemLoader(['.', cfg['project_dir']])

def process_file(files, target, tmpl, ctx):
    print('Processing:', files[0])

    with open(target, 'w') as fd:
        for stmt in tmpl.generate(ctx):
            fd.write(stmt)

        fd.write('\n')

def run(cfg, env):
    if 'globals' in cfg:
        env.globals = cfg['globals']

    env.globals['date'] = str(datetime.now())

    if 'templates' in cfg:
        # Process all templates.
        for template in (cfg['templates'] or []):
            if 'file' not in template:
                continue

            ctx = template['context'] if 'context' in template else {}
            out_file = template['output'] if 'output' in template \
                else template['file'] + '.out'
            out_file = join(cfg['project_dir'], out_file)
            deps = template['dependencies'] if 'dependencies' in template else []

            tmpl = env.get_template(template['file'])
            update_file(deps + [tmpl.filename], out_file, process_file, tmpl, ctx)
