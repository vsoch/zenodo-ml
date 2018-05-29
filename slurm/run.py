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
from urllib.request import urlparse
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
uid = int(sys.argv[1])

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
    if not os.path.exists(dest):
        os.mkdir(dest)
    retval = os.system('tar -xzf %s --directory %s' %(archive, dest))
    if retval == 0:
        return dest

def download_repo(repo):
    '''download a Github repository'''
    tmpdir = tempfile.mkdtemp()
    os.chdir(tmpdir)
    res = os.system('git clone %s' %(repo))
    name = "%s/%s" %(tmpdir, os.path.basename(repo))
    return tmpdir, name


def download_files(filelist):
    '''download a list of files'''
    tmpdir = tempfile.mkdtemp()
    os.chdir(tmpdir)
    for filey in filelist:
        filename = os.path.join(tmpdir, filey.split("/")[-1])   
        print('Downloading %s' %filename)
        with open(filename, "wb") as fh:
            response = requests.get(filey)
            fh.write(response.content)

        # Decompress any files provided
        if os.path.exists(filename):
            if filename.endswith('zip'):
                unzip(filename, tmpdir)
            elif filename.endswith('gz'):
                untar(filename, tmpdir)

    return tmpdir


def download_archive(url):
    '''download a Github repository archive'''
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
        # Clean up download
        os.remove(filename)
    return tmpdir, result
 

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


def process_repo(uid, repo, url, output_folder):
    '''the main function to process the files list for the repo,
       and save a metadata and images pickle to output_folder
    '''
    # Create an output directory
    if not os.path.exists(output_folder):
         os.mkdir(output_folder)

    # Filename according to id
    output_images = os.path.join(output_folder, 'images_%s.pkl' %uid)
    output_meta = os.path.join(output_folder, 'metadata_%s.pkl' %uid)

    # Get file listing
    print('Parsing %s | %s' %(uid, url))
    files = get_files(repo)

    # We don't want to parse github version control
    files = [f for f in files if '.git' not in f]

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

        # Save everything
        pickle.dump(images, open(output_images,'wb'))
        pickle.dump(metadata, open(output_meta,'wb'))



hits = pickle.load(open(records_pkl, 'rb'))
print('Found %s records' %len(hits))

hit = hits[uid]
found = False
links = [y['self'] for y in [x['links'] for x in hit['files']]]
for url in links:

    # Download tar.gz repository
    tmpdir, repo = download_archive(url)

    # if repo is None, try downloading from Github directly
    if repo is None:

        # Didn't use the old download
        shutil.rmtree(tmpdir)

        if 'related_identifiers' in hit['metadata']:
            for resource in hit['metadata']['related_identifiers']:
                if "github" in resource['identifier']:
                    url = urlparse(resource['identifier'])
                    github = '/'.join([x for x in url.path.split('/') if x][0:2])
                    repo = 'https://www.github.com/%s' %github
                    tmpdir, repo = download_repo(repo)
                    found = True

    if repo is not None:
        
        # Save metadata and images pickle to output folder
        process_repo(uid, repo, url, output_folder)
        found = True

# After parsing through all urls, if we didn't find a result, try parsing files
if not found:
    tmpdir = download_files(links)
    process_repo(uid, tmpdir, uid, output_folder)


# Clean up temporary directory
if os.path.exists(tmpdir):
    shutil.rmtree(tmpdir)
