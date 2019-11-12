#!/usr/bin/env python3

import argparse
import os

def setupArgs():
    parser = argparse.ArgumentParser(description='Fix permalinks to be hierarchical in directory')
    parser.add_argument('directory', type=str,
                        help='Directory to recursively fix all .md files.')
    return parser.parse_args()

def fixLink(old, path, name):
    new = []
    for line in old.split('\n'):
        if line and not line.startswith('permalink:'):
            new.append(line)
    
    new.append(f'permalink: {path}/{name[:-3]}')
    return '\n'.join(new) + '\n'

if __name__=="__main__":
    args = setupArgs()

    for dirpath, dirnames, filenames in os.walk(args.directory):
        for filename in filter(lambda a: a.endswith('.md'), filenames):
            with open(os.path.join(dirpath,filename)) as f:
                d = f.read()
                begin = d.find('---')
                end = d.find('---', begin+1)
                frontmatter = d[begin:end]
                new = fixLink(frontmatter, '/'.join(dirpath.split('/')[1:]) , filename)
            with open(os.path.join(dirpath,filename), 'w') as f:
                f.write(d[:begin] + new + d[end:])