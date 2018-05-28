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

import requests
import pickle
import sys
import os

def read_file(file_name):
    with open(file_name) as filey:
        content = filey.read()
    return content

here = os.path.dirname(os.path.abspath(__file__))
if not os.path.exists('%s/.secrets' %here):
    print('You must write Zenodo API key in .secrets file in %s.' %here)
    print('https://zenodo.org/account/settings/applications/tokens/new/')
    sys.exit(1)

ACCESS_TOKEN = read_file('.secrets').strip('\n')
response = requests.get('https://zenodo.org/api/records',
                        params={'access_token': ACCESS_TOKEN,
                                'type': 'software',
                                'size': 1000 })

records = response.json()
hits = records['hits']['hits']
next = records['links']['next']
size = 1000

while next:
    print(next)
    response = requests.get(next, params={'access_token': ACCESS_TOKEN,
                                          'size': size })
    records = response.json()
    if response.status_code == 200:
        hits = hits + records['hits']['hits']
        next = records['links']['next']
    else:
        print(records['message'])
        if size == 500:
            break
        size = 500

# Get unique results by doi
results = dict()
for hit in hits:
    results[hit['id']] = hit

print('Total of %s results.' %len(results))
pickle.dump(results, open('records.pkl','wb'))
