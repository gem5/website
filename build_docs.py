import argparse
import os
from pathlib import Path
from yaml import safe_load, dump

def setupArgs():
    parser = argparse.ArgumentParser(description='Fix permalinks to be hierarchical in directory')
    parser.add_argument('directory', type=str,
                        help='Directory to recursively fix all .md files.')
    return parser.parse_args()

def getPermalink(path):
    return Path(*path.parts[1:]) # skip _pages

def processPage(dirpath, filename, file):
    filedata = file.read()
    begin = filedata.find('---')
    end = filedata.find('---', begin+1)
    meta = safe_load(filedata[begin:end])

    path = Path(dirpath, filename)

    if not meta:
        print(f"Missing yaml front matter for {path}")
        return None

    permalink = getPermalink(path)
    meta['permalink'] = '/' + str(permalink)[:-3] + '/' # trim .md and add /
    if filename == 'index.md':
        meta['permalink'] = '/' + str(permalink.parent) + '/'

    if 'title' not in meta.keys():
        print(f"Missing title for {path}")
        return None

    meta['layout'] = 'documentation'

    if 'order' not in meta.keys():
        meta['order'] = 0

    if filename == 'index.md':
        meta['order'] = -100

    return meta, begin, end, filedata


def processDir(entries, dirpath, parent):
    files = []
    dirs = []
    for p in entries:
        if p.is_file():
            files.append(p)
        elif p.is_dir():
            dirs.append(p)

    pages = []

    for filename in filter(lambda a: a.name.endswith('.md'), files):
        with open(Path(dirpath,filename.name)) as f:
            meta, begin, end, filedata = processPage(dirpath, filename.name, f)
            pages.append(meta)
            if not meta:
                exit(1)
        with open(Path(dirpath,filename.name), 'w') as f:
            f.write('---\n' + dump(meta) + filedata[end:])

    pages.sort(key=lambda d: d['order'])
    if not parent:
        parent = pages[0]['title']

    for p in pages:
        p['parent'] = parent

    for dirname in dirs:
        pages.append(processDir(os.scandir(dirname), dirname, pages[0]['title']))

    pages[0]['subitems'] = pages[1:]

    return pages[0]


if __name__=="__main__":
    args = setupArgs()

    pages = processDir(os.scandir(args.directory), Path(args.directory), '')

    print(dump(pages))
