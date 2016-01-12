import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Shelter(Base):
    __tablename__ = 'shelter'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    address = Column(String(100), nullable=False)
    city = Column(String(50), nullable=False)
    state = Column(String(50), nullable=False)
    zipCode = Column(String(10), nullable=False)
    website = Column(String(100))

class Puppy(Base):
    __tablename__ = 'puppy'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    dateOfBirth = Column(Date)
    gender = Column(String(8))
    weight = Column(Numeric)
    shelter_id = Column(Integer, ForeignKey('shelter.id'))
    shelter = relationship(Shelter)


engine = create_engine('sqlite:///puppyshelter.db')


Base.metadata.create_all(engine)
