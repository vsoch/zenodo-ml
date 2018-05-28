#!/usr/bin/env python

from containertree import ContainerTree
import shutil
import numpy
import tempfile
import pandas
import pickle
import re
import os

here = os.path.abspath(os.path.dirname(__file__))
os.chdir(here)

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


def create_array(ordinal, width=80):
    '''create array from list of ordinals'''
    df = pandas.DataFrame(ordinal).loc[:,0:width-1]
    return df.values


def create_images(filepath, width=80, height=80):
    '''convert a script into an image'''

    with open(filepath,'rb') as fp:
        content = fp.read().decode('utf8', 'ignore')

    # here we get rid of windows newline, replace tab with 4 spaces, lines
    lines = content.replace('\r','').replace('\t','    ').split('\n')

    # We want to "register" to top left (shebang)
    ordinal = []
    start = 0
    finish = start + height

    while finish < len(lines):
        finish = start + height  
        subset = lines[start:finish]

        # Each line in subset padded up to width
        subset = [list(p) + (width - len(p)) * [' '] for p in subset]
        subordinal = []
        for line in subset:
            ordinal.append([ord(x) for x in line])
        start = finish
        finish = start + height
        
    # Here we might have remainder, we can keep and not use if wanted
    if start < len(lines):
        finish = len(lines) - 1
        if start==finish:
            subset = lines[start]
        else:
            subset = lines[start:finish]

        # Each line in subset padded up to width
        subset = [list(p) + (width - len(p)) * [' '] for p in subset]
        for line in subset:
            ordinal.append([ord(x) for x in line])

    # Ordinal we can convert to a numpy array
    ordinal = create_array(ordinal, width)

    print('%s has %s %sx%s images' %(filepath, len(ordinal), width, height))
    return ordinal


hits = pickle.load(open('%s/records.pkl' %here, 'rb'))
print('Found %s records' %len(hits))

# Create an output directory
output_data = '%s/data' %here
if not os.path.exists(output_data):
    os.mkdir(output_data)

# Skip some, too big and annoying for my tiny computer
seen_data = '%s/seen.pkl' %here
if os.path.exists(seen_data):
    seen = pickle.load(open(seen_data,'rb'))
else:
    seen = []

print('Seen %s records' %len(seen))
missed = []

for uid, hit in hits.items():
    if 'related_identifiers' in hit['metadata']:
        for resource in hit['metadata']['related_identifiers']:
            if "github" in resource['identifier'] and uid not in seen:
                url = resource['identifier']

                # Cache seen in case need to start over
                seen.append(uid)
                pickle.dump(seen, open(seen_data,'wb'))

                # If tree in link, grab specific branch 
                process = True
                match = re.search('(?P<repo>.+)/tree/(?P<branch>.+)', url)
                repo = match.group('repo')

                # No idea what gcube is, but it has a gazillion entries
                if repo is not None:
                    if "gcube" not in repo:
                        repo = download_repo(repo, match.group('branch'))
                    else:
                        process = False
                else:
                    missed.append(uid)
                    process = False

                if process is True:

                    # Get file listing
                    print('Parsing %s | %s' %(uid, url))
                    files = get_files(repo)

                    # Filename according to id
                    output_folder = os.path.join(output_data, '%s' %hit['id'])
                    output_images = os.path.join(output_folder, 'images_%s.pkl' %hit['id'])
                    output_ordinal = os.path.join(output_folder, 'ordinal_%s.pkl' %hit['id'])
                    output_meta = os.path.join(output_folder, 'metadata_%s.pkl' %hit['id'])

                    if not os.path.exists(output_folder):
                        os.mkdir(output_folder)

                    # For each file, save pickle of images
                    tree = make_containertree(uid, files, basepath=repo)
                    images = dict()
                
                    for f in files:
                        name = f.replace('%s/'% repo, '')
                        if '.git' not in name:
   
                            # We will give the user ordinal
                            images[name] = create_images(f)

                    # Metadata is tree and other hit
                    metadata = {'tree': tree, 'hit': hit}

                    # Clean up temporary directory
                    shutil.rmtree(repo)

                    # Save everything
                    pickle.dump(images, open(output_images,'wb'))
                    pickle.dump(metadata, open(output_meta,'wb'))
