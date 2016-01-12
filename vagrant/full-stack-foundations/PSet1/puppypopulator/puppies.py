from sqlalchemy import Table, Column, ForeignKey, Integer, String, Date, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()

puppy_adopter = Table('puppy_adopter', Base.metadata,
                        Column('puppy_id', Integer, ForeignKey('puppy.id')),
                        Column('adopter_id', Integer, ForeignKey('adopter.id'))
                    )    

class Shelter(Base):
    __tablename__ = 'shelter'
    id = Column(Integer, primary_key = True)
    name =Column(String(80), nullable = False)
    address = Column(String(250))
    city = Column(String(80))
    state = Column(String(20))
    zipCode = Column(String(10))
    website = Column(String)
    maximum_capacity = Column(Integer)
    current_occupancy = Column(Integer)
    puppies = relationship('Puppy', back_populates = 'shelter')

class Puppy(Base):
    __tablename__ = 'puppy'
    id = Column(Integer, primary_key = True)
    name = Column(String(250), nullable = False)
    gender = Column(String(6), nullable = False)
    dateOfBirth = Column(Date)
    weight = Column(Numeric(10))
    shelter_id = Column(Integer, ForeignKey('shelter.id'))
    shelter = relationship('Shelter', back_populates = 'puppies')
    profile = relationship('Profile', uselist = False, back_populates = 'puppy')
    adopters = relationship('Adopter', secondary = puppy_adopter, back_populates = 'puppies')

class Profile(Base):
    __tablename__ = 'profile'
    id = Column(Integer, primary_key = True)
    picture = Column(String, nullable = True)
    description = Column(String(100), nullable = True)
    special_needs = Column(String(250), nullable = True)
    puppy_id = Column(Integer, ForeignKey('puppy.id'))
    puppy = relationship('Puppy', back_populates = 'profile')

class Adopter(Base):
    __tablename__ = 'adopter'
    id = Column(Integer, primary_key = True)
    name =Column(String(80), nullable = False)
    address = Column(String(250))
    city = Column(String(80))
    state = Column(String(20))
    zipCode = Column(String(10))
    puppies = relationship('Puppy', secondary = puppy_adopter, back_populates = 'adopters')

engine = create_engine('sqlite:///puppyshelter.db')
 

Base.metadata.create_all(engine)