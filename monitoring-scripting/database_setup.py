from sqlalchemy import Column, ForeignKey, Integer, String ,Date ,DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Device(Base):
    __tablename__ = 'device'

    id = Column(Integer, primary_key=True)
    ip = Column(String(250), nullable=False)
    name = Column(String(250), nullable=False)
    type = Column(String(250))
    model= Column(String(250))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'ip': self.ip,
            'type' : self.type
        }

class Alarm(Base):
    __tablename__ = 'alarm'

    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    detail = Column(String(1000), nullable=False)
    alarm_time = Column(DateTime)
    device_ip = Column(String, ForeignKey('device.ip'))
    #device_name = Column(String, ForeignKey('device.name'))
    device = relationship(Device)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'device_name': self.device_name,
        }



engine = create_engine('sqlite:///alarmsAndDevices.db')


Base.metadata.create_all(engine)
