from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
 
from puppies import Base, Shelter, Puppy
#from flask.ext.sqlalchemy import SQLAlchemy
from random import randint
from datetime import date, timedelta
import random


engine = create_engine('sqlite:///puppyshelter.db')

Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)

session = DBSession()

# 1. Query all of the puppies and return the results in ascending alphabetical order
print "Query 1"
query = session.query(Puppy).order_by(Puppy.name)

for row in query.all():
	print row.id, row.name, row.gender, row.dateOfBirth, row.weight

# 2. Query all of the puppies that are less than 6 months old organized by the youngest first
print "Query 2"
query = session.query(Puppy).filter(Puppy.dateOfBirth.between(date.today() - timedelta(days=180), date.today())).order_by(desc(Puppy.dateOfBirth))

for row in query.all():
	print row.id, row.name, row.gender, row.dateOfBirth, row.weight


# 3. Query all puppies by ascending weight
print "Query 3"
query = session.query(Puppy).order_by(Puppy.weight)

for row in query.all():
	print row.id, row.name, row.gender, row.dateOfBirth, row.weight


# 4. Query all puppies grouped by the shelter in which they are staying
print "Query 4"
query = session.query(Puppy).group_by(Puppy.shelter_id)

for row in query.all():
	print row.shelter_id, row.id, row.name, row.gender, row.dateOfBirth, row.weight


