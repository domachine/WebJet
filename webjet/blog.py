import os.path
import re

from os import listdir

import yaml


PRIORITY = 1

def init(cfg, env_cfg):
    pass

def _scan_post(post, out_name):
    sep_regexp = re.compile('^\\-\\-\\- *$')

    post_header = ''

    with open(post, 'r') as post_file, open(out_name, 'w') as out_file:
        sep_found = False
        title_read = False

        for line in post_file:
            if not sep_found:
                # Scan title
                if sep_regexp.match(line):
                    sep_found = True
                    post_header = yaml.load(post_header)
                else:
                    post_header += line
            else:
                if not title_read:
                    post_title = None
                    if isinstance(post_header, str):
                        post_title = post_header
                    else:
                        post_title = post_header['title'] if 'title' in post_header else ''

                    print('{% call cb(\'' +
                          post_title.replace('\'', '\\\'') +
                          '\') %}',
                          file=out_file)

                    title_read = True

                print(line, file=out_file)

        print('{% endcall %}', file=out_file)

def _file_key(x):
    m = re.match('^([0-9]*).*$', x)
    if m:
        if m.group(1):
            return int(m.group(1))
        else:
            return 0
    else:
        return 0

def run(cfg, env):
    if 'blogs' not in cfg:
        return

    for blog in (cfg['blogs'] or []):
        blog_dir = blog['name'] if 'name' in blog else None
        blog_dir = blog['dir'] if 'dir' in blog else None

        if not blog_dir:
            continue

        blog_dir = os.path.join(cfg['project_dir'], blog_dir)

        if not os.path.isdir(blog_dir):
            raise ValueError("blog_dir value `{0}' is not a directory".format(blog_dir))

        with open(os.path.join(blog_dir, 'index'), 'w') as idx_file:
            print('{% macro init(cb) %}', file=idx_file)

            files = os.listdir(blog_dir)
            files.sort(key=_file_key, reverse=True)

            for f in files:
                if f.endswith('.post'):
                    out_name = os.path.join(blog_dir, f.replace('.post', '.html'))
                    _scan_post(os.path.join(blog_dir, f), out_name)

                    print('{% include \'' + out_name + '\' %}', file=idx_file)

            print('{% endmacro %}', file=idx_file)
