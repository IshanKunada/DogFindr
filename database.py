# Import the 'db' object and the 'User' model class from the 'app' module.
from app import app, db, User, Shelter, Dog

# Import the 'generate_password_hash' function from the 'werkzeug.security' module.
# This function is used to create a hashed version of a password.
from werkzeug.security import generate_password_hash

# Need to set up application context while using the db functions
with app.app_context():
	exit()
	
	# If any tables currently exist, delete them
	# This is so we can start fresh and make new tables that have the updated changes
	db.drop_all()

	# Create all the tables defined in the app's models.
	# If tables already exist, this won't recreate them.
	db.create_all()

	# Generate a hashed version of the string 'password123' using the scrypt hashing algorithm.
	hashed_pw = generate_password_hash('password123', method='scrypt')

	# Create a new user instance with the username 'admin' and the hashed password.
	new_user = User(email='admin@gmail.com', password=hashed_pw)

	new_shelter = Shelter(address='230 Congress Street', name = 'Acadiana Animal Aid', image = 'https://s3.us-east-1.amazonaws.com/files.galaxydigital.com/5550/agency/137736.jpg?20230808183737', description = 'Place in Acadiana')
	lafayette_shelter = Shelter(address='229 Congress Street', name = 'Lafayette Animal Aid', image = 'https://s3.us-east-1.amazonaws.com/files.galaxydigital.com/5550/agency/137736.jpg?20230808183737', description = 'Place in Lafayette')

	new_dog = Dog(name = 'Lucky', age = 6, breed = 'Golden Retreiver')
	dog_2 = Dog(name = 'Mike', age = 4, breed = 'Doberman')
	# Add the new user instance to the current session's staging area.
	# This prepares it to be stored in the database.
	db.session.add(new_user)
	db.session.add(new_shelter)
	db.session.add(lafayette_shelter)
	db.session.add(new_dog)
	db.session.add(dog_2)

	# Commit the changes made in the session to the database.
	# This will save the new user in the 'users' table.
	db.session.commit()

	# delete all users