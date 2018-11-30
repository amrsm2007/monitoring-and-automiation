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

devices = "monitoring-scripting/devices.txt"
host_name = "monitoring-scripting/host_name.txt"
with open(devices, 'r') as f:
    devices = f.readlines()
    devices = [x.strip() for x in devices]

with open(host_name, 'r') as f:
    hosts = f.readlines()
    hosts = [x.strip() for x in hosts]

# Create dummy user
for device, host in zip(devices, hosts):
    x=Device_db(ip=device,name=host)
    session.add(x)
    session.commit()





print ("added menu items!")