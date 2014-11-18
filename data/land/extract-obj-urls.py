

## get all urls of objects

from bs4 import BeautifulSoup

import os

fns = filter(lambda x:x.startswith('index.php'), os.listdir('.'))

urls = []

for fn in fns:

    html_doc = open(fn).read()

    soup = BeautifulSoup(html_doc)

    urls += filter(lambda a: 'showobj.php?' in a, [x.get('href') for x in soup.findAll('a', {'class': 'link2'})])

open('obj-urls.txt', 'w').write('\n'.join(urls))