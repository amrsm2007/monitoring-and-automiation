from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Device as Device_db,Alarm

engine = create_engine('sqlite:///alarmsAndDevices.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

devicis=session.query(Device_db).all()
#for i in devicis:
    #print ( i.name +"  :  "+ i.ip)

data=session.query(Alarm).filter_by(id=50).first()
print (data)

is_it_repeated = session.query(Alarm).filter_by(detail=data).first()
print(is_it_repeated)