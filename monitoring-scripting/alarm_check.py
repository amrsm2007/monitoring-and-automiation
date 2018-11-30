from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Device as Device_db,Alarm
from jnpr.junos import Device
import time
from netmiko import ConnectHandler
import os
duration = 1  # second
freq = 440  # Hz

# Connect to Database and create database session
engine = create_engine('sqlite:///alarmsAndDevices.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

devices=session.query(Device_db).all()

def chaissAlamrm():
    while True:
        DBSession = sessionmaker(bind=engine)
        session = DBSession()


        for device in devices:
            print (device.name)
            try:
                with Device(host=device.ip, user="a.abdelwahab", passwd="VGPxzbXV", port="22", gather_facts=False) as dev:
                    data = dev.rpc.get_alarm_information({"format": "text"}).text
                    #print (data)
                    #print (len(data.splitlines()))
                    if len(data.splitlines())>2 and "Require a Fan Tray upgrade" not in data:
                        #alarm=" there is chassis alarm on : " +device.name + " as below " +"\n"+ data +"\n"+"_"*100 +"\n"


                        x=Alarm(detail=data,device_ip=device.ip,alarm_time=time.ctime())
                        is_it_repeated = session.query(Alarm).filter_by(detail=x.detail).first()
                        print (x.detail)
                        print(is_it_repeated)



                        if is_it_repeated == None:
                            print (x.alarm_time)
                            session.add(x)
                            session.commit()


                    else:
                        print (" NO active allarm on : "+ device.name)

            except:
                print("check device")

if __name__ == '__main__':
    # test1.py executed as script
    # do something
    chaissAlamrm()

