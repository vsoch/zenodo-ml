#!/usr/bin/env python

from containertree import ContainerTree
import shutil
import tempfile
import pickle
import re
import os

here = os.path.abspath(os.path.dirname(__file__))

def download_repo(repo, branch):
    '''download a Github repository'''
    tmpdir = tempfile.mkdtemp()
    os.chdir(tmpdir)
    res = os.system('git clone -b %s %s' %(branch, repo))
    if res != 0:
        res = os.system('git clone %s' %(repo))
    return tmpdir
 

def get_files(path):
    '''return listing of files'''
    f = []
    for (dirpath, dirnames, filenames) in os.walk(path):
        for filename in filenames:
            fullpath = os.path.join(dirpath, filename)
            if os.path.isfile(fullpath):
                f.append(os.path.abspath(fullpath))
    return f


def make_containertree(uid, files, basepath=None):
    '''make and return a container tree'''
    filelist = []
    for f in files:
        size = os.path.getsize(f)
        name = f.replace('%s/' %basepath,'')
        filelist.append({'Name': name, 'Size': size})
    tree = ContainerTree(filelist, tag=uid)
    return tree


def create_images(filepath, width=80, height=80):
    '''convert a script into an image'''
    with open(filepath,'rb') as fp:
        content = fp.read().decode('utf8', 'ignore')

    # here we get rid of windows newline, replace tab with 4 spaces, lines
    lines = content.replace('\r','').replace('\t','    ').split('\n')

    # We want to "register" to top left (shebang)
    finished = []
    start = 0
    finish = start + height

    while finish < len(lines):
        finish = start + height  
        subset = lines[start:finish]

        # Each line in subset padded up to width
        subset = [list(p) + (width - len(p)) * [' '] for p in subset]
        finished.append(subset)
        start = finish
        finish = start + height
        
    # Here we might have remainder, we can keep and not use if wanted
    if start < len(lines):
        finish = len(lines) - 1
        subset = lines[start:finish]

        # Each line in subset padded up to width
        subset = [list(p) + (width - len(p)) * [' '] for p in subset]
        finished.append(subset)

    print('%s has %s %sx%s images' %(filepath, len(finished), width, height))
    return finished


hits = pickle.load(open('records.pkl', 'rb'))
print('Found %s records' %len(hits))

# Create an output directory
output_data = '%s/data' %here
if not os.path.exists(output_data):
    os.mkdir(output_data)

# Skip some, too big and annoying for my tiny computer
if os.path.exists('seen.pkl'):
    seen = pickle.load(open('seen.pkl','rb'))
else:
    seen = [806345]

missed = []

for uid, hit in hits.items():
    if 'related_identifiers' in hit['metadata']:
        for resource in hit['metadata']['related_identifiers']:
            if "github" in resource['identifier'] and uid not in seen:
                url = resource['identifier']
                print('Parsing %s | %s' %(uid, url)) 

                seen.append(uid)

                # If tree in link, grab specific branch 
                match = re.search('(?P<repo>.+)/tree/(?P<branch>.+)', url)
                repo = match.group('repo')
                if repo is not None:
                    repo = download_repo(repo, match.group('branch'))
                else:
                    missed.append(uid)
                    continue

                # Get file listing
                files = get_files(repo)

                # Filename according to id
                output_folder = os.path.join(output_data, '%s' %hit['id'])
                output_images = os.path.join(output_folder, 'images_%s.pkl' %hit['id'])
                output_meta = os.path.join(output_folder, 'metadata_%s.pkl' %hit['id'])

                if not os.path.exists(output_folder):
                    os.mkdir(output_folder)

                # For each file, save pickle of images
                tree = make_containertree(uid, files, basepath=repo)
                images = dict()
                
                for f in files:
                    name = f.replace('%s/'% repo, '')
                    if '.git' not in name:
                        subset = create_images(f)
                        images[name] = subset

                # Metadata is tree and other hit
                metadata = {'tree': tree, 'hit': hit}

                # Clean up temporary directory
                shutil.rmtree(repo)

                # Save everything
                pickle.dump(images, open(output_images,'wb'))
                pickle.dump(metadata, open(output_meta,'wb'))
                pickle.dump(seen, open('seen.pkl','wb'))

