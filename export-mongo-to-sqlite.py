# -*- coding: utf-8 -*-

from sqlalchemy import Table, MetaData, Column, ForeignKey, Integer, String, Float, Unicode, Sequence, create_engine

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker

import pymongo

Base = declarative_base()

class Lands(Base):
    __tablename__ = 'lands'

    id = Column(Integer, Sequence('land_id_seq'), primary_key=True) 

    # 總價
    price = Column(Integer)

    # 平米
    area = Column(Float)

    # 位置
    location = Column(Unicode)

    # 類別
    usage = Column(Unicode)

    # 案名
    name = Column(Unicode)

    # 案號
    oid = Column(String)

    def __repr__(self):
        return "<Lands(id='%d')>" % (self.id)

if __name__ == '__main__':

    co = pymongo.Connection('localhost')['workshop']['lands.info']

    engine = create_engine('sqlite:///lands.db3', echo=False)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()
    
    # obj = Lands(price=17250000, area=4072.73, location=u'宜蘭縣員山鄉', usage=u'農地', name=u'近縣政中心大農地')

    _total = co.find().count()
    for i,mdoc in enumerate(co.find()):
        obj = Lands(oid=mdoc[u'案號'], price=mdoc[u'總價'], area=mdoc[u'平米'], location=mdoc[u'位置'], usage=mdoc[u'類別'], name=mdoc[u'案名'])
        session.add(obj)
        print 'Add %d/%d' % (i+1, _total)

    print 'Commit changes...'
    session.commit()

    print 'Done.'
    session.close()