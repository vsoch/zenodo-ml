#!/usr/bin/env python
#
# Copyright (C) 2018 Vanessa Sochat.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public
# License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


from containertree import ContainerTree
import shutil
import numpy
import requests
import tarfile
import tempfile
import pandas
import pickle
import zipfile
import sys
import re
import os

# The zenodo uid
uid = sys.argv[1]

# Output folder for pickles
output_folder = sys.argv[2]

# Records Pickle
records_pkl = sys.argv[3]

# upper limit of file size, in bytes
size_limit = 100000


def unzip(archive, dest):
    '''unzip an archive to a destination'''
    with zipfile.ZipFile(archive, 'r') as zippy:
        zippy.extractall(dest)
    return dest

def untar(archive, dest):
    '''untar an archive to a destination (lazy way)'''
    retval = os.system('tar -xf %s --directory %s' %(archive, dest))
    if retval == 0:
        return dest

def download_repo(url):
    '''download a Github repository'''
    tmpdir = tempfile.mkdtemp()
    os.chdir(tmpdir)
    filename = os.path.join(tmpdir, url.split("/")[-1])   
    with open(filename, "wb") as fh:
        response = requests.get(url)
        fh.write(response.content)

    result = None
    dest = ''.join(filename.split('.')[0:-1])
    if os.path.exists(filename):
        if filename.endswith('zip'):
            result = unzip(filename, dest)
        elif filename.endswith('gz'):
            result = untar(filename, dest)
    return result
 

def get_files(path):
    '''return listing of files'''
    f = []
    for (dirpath, dirnames, filenames) in os.walk(path):
        for filename in filenames:
            fullpath = os.path.join(dirpath, filename)
            if os.path.isfile(fullpath):
                size = os.path.getsize(fullpath)
                if size <= size_limit:
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

hits = pickle.load(open(records_pkl, 'rb'))
print('Found %s records' %len(hits))

hit = hits[uid]
links = [y['self'] for y in [x['links'] for x in hits['files']]]
for url in links:

    # Download tar.gz repository
    repo = download_repo(url)

    if repo is not None:

        # Create an output directory
        if not os.path.exists(output_folder):
             os.mkdir(output_folder)

        # Filename according to id
        output_images = os.path.join(output_folder, 'images_%s.pkl' %hit['id'])
        output_meta = os.path.join(output_folder, 'metadata_%s.pkl' %hit['id'])

        # If we already have done it, skip and exit
        if os.path.exists(output_images):
            size = os.path.getsize(output_images) 
            if size > 0:
                print('Job already done!')
                sys.exit(0)

        # Get file listing
        print('Parsing %s | %s' %(uid, url))
        files = get_files(repo)

        # For each file, save pickle of images
        tree = make_containertree(uid, files, basepath=repo)
        images = dict()
                
        for f in files:

            name = f.replace('%s/'% repo, '')

            # Limit size to not use images, etc.
            size = os.path.getsize(f) 
            if size < size_limit:
   
                # We will give the user ordinal
                try:
                    images[name] = create_images(f)
                except:
                    pass

            # Metadata is tree and other hit
            metadata = {'tree': tree, 'hit': hit}

            # Clean up temporary directory
            shutil.rmtree(repo)

            # Save everything
            pickle.dump(images, open(output_images,'wb'))
            pickle.dump(metadata, open(output_meta,'wb'))
