#!/usr/bin/env python

import requests
import pickle

def read_file(file_name):
    with open(file_name) as filey:
        content = filey.read()
    return content

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
