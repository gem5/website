#!/usr/bin/env python3

import argparse
import os
from yaml import safe_load, dump

def setupArgs():
    parser = argparse.ArgumentParser(description='Fix permalinks to be hierarchical in directory')
    parser.add_argument('directory', type=str,
                        help='Directory to recursively fix all .md files.')
    parser.add_argument('action', help='Action to take',
                        type=str, default=None, choices=['yaml', 'fixlinks'])
    return parser.parse_args()

# TODO: Convert to use yaml
def fixLink(old, path, name):
    new = []
    for line in old.split('\n'):
        if line and not line.startswith('permalink:'):
            new.append(line)

    if name == 'index.md':
        url = f'/{path}/'
    else:
        url = f'/{path}/{name[:-3]}/'

    new.append(f'permalink: {url}')
    return '\n'.join(new) + '\n'

def getTitle(frontmatter):
    data = safe_load(frontmatter)
    return data['title']

def getUrl(frontmatter):
    data = safe_load(frontmatter)
    return data['permalink']

if __name__=="__main__":
    args = setupArgs()

    pages = []

    for dirpath, dirnames, filenames in os.walk(args.directory):
        for filename in filter(lambda a: a.endswith('.md'), filenames):
            with open(os.path.join(dirpath,filename)) as f:
                d = f.read()
                begin = d.find('---')
                end = d.find('---', begin+1)
                frontmatter = d[begin:end]
                path = '/'.join(dirpath.split('/')[1:])
                new = fixLink(frontmatter, path, filename)
            if args.action == 'fixlinks':
                with open(os.path.join(dirpath,filename), 'w') as f:
                    f.write(d[:begin] + new + d[end:])
            else:
                if new != frontmatter:
                    d_new = safe_load(new)
                    d_old = safe_load(frontmatter)
                    if d_new['permalink'] != d_old['permalink']:
                        print(f"Warning. Need to update permalink for {dirpath}/{filename}.")
            if args.action == 'yaml':
                title = getTitle(frontmatter)
                url = getUrl(frontmatter)
                d = {'page': title, 'url': url}
                pages.append(d)

    if args.action == 'yaml':
        print(dump(pages))

