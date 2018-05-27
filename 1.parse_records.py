#!/usr/bin/env python

import pickle

hits = pickle.load(open('records.pkl', 'rb'))
print('Found %s records' %len(hits))

count=0
for uid, hit in hits.items():
    if 'related_identifiers' in hit['metadata']:
        print(hit['metadata']['related_identifiers'])
        count+=1
