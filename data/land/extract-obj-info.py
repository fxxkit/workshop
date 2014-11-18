# coding: utf-8

from bs4 import BeautifulSoup

import os

root = 'yes319-Yilan-objs'

fns = filter(lambda x:x.startswith('showobj.php'), os.listdir(root))

urls = []

import pymongo

db = pymongo.Connection('localhost')['workshop']
# db = pymongo.Connection('doraemon.iis.sinica.edu.tw')['workshop']
co = db['lands']

_total = len(fns)

for i,fn in enumerate(fns):

    print 'process %s (%d/%d)' % (fn, i+1, _total)

    html_doc = open(os.path.join(root,fn)).read()

    soup = BeautifulSoup(html_doc)

    try:
        table = soup.findAll('table', {'width': '720'})[0]
    except IndexError:
        continue

    keys, vals = [], []
    entries = table.findAll('td')
    for entry in entries:
        if not 'class' in entry.attrs:
            continue

        if 'h1' in entry.attrs['class']:
            # key
            keys.append( entry.text.strip() )

        elif 'td3' in entry.attrs['class'] or 'td4' in entry.attrs['class']:
            # val
            vals.append( entry.text.strip() )

    info = dict(zip(keys, vals))

    # print info
    co.insert(info)

