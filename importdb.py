# NOT USED

from sqlalchemy import create_engine
engine = create_engine('sqlite:////Users/ishan/projects/dogshelter/DogShelter.db', echo=True)

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

Base = automap_base()
Base.prepare(engine, reflect=True) 

DogMedical = Base.classes.DogMedical

session = Session(engine)