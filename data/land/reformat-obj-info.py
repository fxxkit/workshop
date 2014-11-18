# coding: utf-8

import pymongo, re

db = pymongo.Connection('localhost')['workshop']
# db = pymongo.Connection('doraemon.iis.sinica.edu.tw')['workshop']
src = db['lands.raw']
dest = db['lands.info']
# processing specific data
# 坪數
# 總價
# 位置
# 類別
# 更新日期

required = {u'坪數', u'總價'}

_total = src.find().count()

for i, mdoc in enumerate(src.find()):

    ## check if all required fields exist in this object
    if not len(filter(lambda x:x in required, mdoc.keys())) == len(required):
        continue

    print 'process object %d/%d' % (i+1, _total)

    ## 坪數
    # 1,232坪 ( 4072.73 平方公尺)
    # '1,232\u576a\xa0( 4072.73 \u5e73\u65b9\u516c\u5c3a)'
    # get m^2
    area_m2 = float(mdoc[u'坪數'].split(u'平方公尺')[0].split('(')[-1].strip())
    mdoc[u'平米'] = area_m2
    mdoc[u'坪數'] = area_m2/3.30579
    mdoc[u'分地'] = area_m2/969.918
    mdoc[u'甲地'] = area_m2/9699.18


    ## 總價
    # 2,763.88萬
    # 2,467萬\t\t\t,價格可議
    # 1.0166億
    # 3,917.76萬\t\t\t,價格可議
    unit_ten_th = 10000.0 # 萬
    unit_hand_mi = 100000000.0 # 億
    price = float(re.findall(r'[0-9.]+', mdoc[u'總價'].replace(',',''))[0])
    if u'萬' in mdoc[u'總價']:
        unit = unit_ten_th
    elif u'億' in mdoc[u'總價']:
        unit = unit_hand_mi
    else:
        unit = 1.0
    total_price = price*unit

    mdoc[u'總價'] = total_price
    mdoc[u'萬'] = total_price/unit_ten_th
    mdoc[u'億'] = total_price/unit_hand_mi

    # 1 平方公尺 = 0.3025 坪
    # 1 坪 = 3.30579 平方公尺
    # 1 分 = 969.918 平方公尺
    mdoc[u'萬_坪'] = mdoc[u'萬']/mdoc[u'坪數']
    mdoc[u'萬_平米'] = mdoc[u'萬']/mdoc[u'平米']
    mdoc[u'萬_分'] = mdoc[u'萬']/mdoc[u'分地']

    dest.insert(mdoc)

