# Import necessary modules
from app import app, db, Users, Adopterinfo, Dogadoptionneeds, Dogmedical, Fosterinfo, Shelters
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash

# Path to your SQLite database
db_path = 'DogShelterOriginal.db'

# Create an engine and reflect the database schema
engine = create_engine(f'sqlite:///{db_path}')
Base = automap_base()
Base.prepare(engine, reflect=True)

# Map the existing tables to the new SQLAlchemy models
ReflectedAdopterinfo = Base.classes.AdopterInfo
ReflectedDogadoptionneeds = Base.classes.DogAdoptionNeeds
ReflectedDogmedical = Base.classes.DogMedical
ReflectedFosterinfo = Base.classes.FosterInfo
ReflectedShelters = Base.classes.Shelters
ReflectedUsers = Base.classes.Users

# Create a session
session = Session(engine)

# Query all rows from the existing SQLite database
adopterinfo_rows = session.query(ReflectedAdopterinfo).all()
dogadoption_rows = session.query(ReflectedDogadoptionneeds).all()
dogmedical_rows = session.query(ReflectedDogmedical).all()
fosterinfo_rows = session.query(ReflectedFosterinfo).all()
shelters_rows = session.query(ReflectedShelters).all()
users_rows = session.query(ReflectedUsers).all()

# Convert the rows into SQLAlchemy objects
adopterinfo_objects = [Adopterinfo(
    ID=row.ID,
    TagNumber=row.TagNumber,
    Name=row.Name,
    Adopter=row.Adopter,
    Phone=row.Phone,
    Email=row.Email,
    AdoptionDate=row.AdoptionDate,
    Contract=row.Contract,
    PaymentConfirmation=row.PaymentConfirmation,
    CheckNumber=row.CheckNumber,
    Email2=row.Email2,
    Address=row.Address,
    City=row.City,
    St=row.St,
    Zip=row.Zip,
    AdoptercellPhone=row.AdoptercellPhone
) for row in adopterinfo_rows]

dogadoption_objects = [Dogadoptionneeds(
    ID=row.ID,
    TagNumber=row.TagNumber,
    Name=row.Name,
    OtherdogsPlay=row.OtherdogsPlay,
    OtherdogsParalelllive=row.OtherdogsParalelllive,
    Cats=row.Cats,
    Kids=row.Kids,
    Housetrained=row.Housetrained,
    Cratetrained=row.Cratetrained,
    leashwalk=row.leashwalk,
    Doorescape=row.Doorescape,
    Digger=row.Digger,
    Vocal=row.Vocal,
    FireworksFear=row.FireworksFear,
    Specialneeds=row.Specialneeds,
    Notes=row.Notes
) for row in dogadoption_rows]

dogmedical_objects = [Dogmedical(
    ID=row.ID,
    TagNumber=row.TagNumber,
    Dated=row.Dated,
    Name=row.Name,
    Sex=row.Sex,
    Breed=row.Breed,
    picture=row.picture,
    DateofBirth=row.DateofBirth,
    Status=row.Status,
    Source=row.Source,
    MicrochipNumber=row.MicrochipNumber,
    Type=row.Type,
    VaccinationDate=row.VaccinationDate,
    VaccPaperworkReceived=row.VaccPaperworkReceived
) for row in dogmedical_rows]

fosterinfo_objects = [Fosterinfo(
    ID=row.ID,
    TagNumber=row.TagNumber,
    Name=row.Name,
    Foster=row.Foster,
    Phone=row.Phone,
    Email=row.Email,
    Fosterspets=row.Fosterspets
) for row in fosterinfo_rows]

shelters_objects = [Shelters(
    id=row.id,
    name=row.name,
    address=row.address
) for row in shelters_rows]

users_objects = [Users(
    email=row.email,
    password=row.password
) for row in users_rows]

# Use the application context to interact with the database
with app.app_context():
    # Drop all tables if needed (be cautious with this step)
    db.drop_all()

    # Create all tables defined in the app's models
    db.create_all()

    # Add the reflected objects to the new database session
    db.session.add_all(adopterinfo_objects)
    db.session.add_all(dogadoption_objects)
    db.session.add_all(dogmedical_objects)
    db.session.add_all(fosterinfo_objects)
    db.session.add_all(shelters_objects)
    db.session.add_all(users_objects)

    # Optionally, add a new user with a hashed password
    hashed_pw = generate_password_hash('12341234', method='scrypt')
    new_user = Users(email='admin@gmail.com', password=hashed_pw)
    db.session.add(new_user)

    # Commit the changes to the database
    db.session.commit()
