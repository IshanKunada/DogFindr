#make sign up page
#finish building out home page
#come up with classes for the dogs

from flask import Flask, render_template, request, flash, redirect, url_for
from flask_login import login_required, login_manager, login_user, logout_user, current_user, LoginManager, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/ishan/projects/dogshelter/DogShelter.db'
app.config['FLASK_DEBUG']=1
app.secret_key = "1234567"  # TODO: use os.getenv()

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Get existing tables from SQLite db

from sqlalchemy import create_engine
engine = create_engine('sqlite:////Users/ishan/projects/dogshelter/DogShelter.db', echo=True)

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

Base = automap_base()
Base.prepare(engine, reflect=True) 

Users = Base.classes.Users
Shelters = Base.classes.Shelters
Dogs = Base.classes.DogMedical
AdoptionNeeds = Base.classes.DogAdoptionNeeds

admins = ['ishan.kunada@gmail.com']

class Users(UserMixin, db.Model):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password, method='scrypt')

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
# class Shelters(db.Model):
#     __tablename__ = 'shelter'
#     __table_args__ = {'extend_existing': True}
#     id = db.Column(db.Integer, primary_key=True)
#     address = db.Column(db.String(30), unique=True)
#     name = db.Column(db.String(40), unique=True)
#     image = db.Column(db.String(256))
#     description = db.Column(db.String(256))
# class Dogs(db.Model):
#     __tablename__ = 'dog'
#     __table_args__ = {'extend_existing': True}
#     id = db.Column(db.Integer, primary_key=True)
#     breed = db.Column(db.String(30))
#     age = db.Column(db.Integer)
#     name = db.Column(db.String(30))
    

@login_manager.user_loader
def load_user(user_id):
  """
  Loads a user from the database based on the user_id provided.
  Returns the User object corresponding to the user_id.
  """
  return Users.query.get(int(user_id))

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    #shelters = Shelters.query.all()
    #print(shelters)
    # dogs = Dogs.query.all()
    with app.app_context():
        session = Session(db.engine)
        dogs = session.query(Dogs).all()
        session.close()

        if request.method == 'POST' :
            try:
                search = request.form.get('search')
                print(search)
                return render_template("home.html", dogs = dogs)     
            except Exception as e:
                print(e)
                flash("Something went wrong. Please try again.")
                return redirect(url_for('home', dogs = dogs))
        else:
            return render_template("home.html", dogs = dogs)


@app.route('/createaccount', methods=['GET', 'POST'])
def createaccount():
  	# sending data
    if request.method == 'POST':
        try: 
            email = request.form.get('email')
            password = request.form.get('password')
            confirmpassword = request.form.get('confirmpassword')
            if password == confirmpassword and len(password)>7:
                hashed_pw = generate_password_hash( password, method='scrypt')
                new_user = Users(email=email, password=hashed_pw)
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('home'))
            elif len(password)<=7:
                flash("Password must be at least 8 characters.")
                return redirect(url_for('createaccount'))
            else:
                flash('Password and confirm password must be the same.')
                return redirect(url_for('createaccount'))
    # just viewing the page, no data sent
        except Exception as e:
            print(e)
            flash("Something went wrong. Please try again.")
            return redirect(url_for('createaccount'))
    else:
    	return render_template('createaccount.html')
    
@app.route('/login', methods=['GET', 'POST'])
def login():
  	# sending data
    try:
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            user = Users.query.filter_by(email=email).first()
            if user and check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('home'))
            else:
                flash('Invalid login credentials!')
                return redirect(url_for('login'))
        # just viewing the page, no data sent
        else:
            return render_template('login.html')
    except Exception as e:
        print(e)
        flash("Something went wrong. Please try again.")
        return redirect(url_for('login'))
    
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/resources')
def resources():
    try:
        with app.app_context():
            session = Session(db.engine)
            shelters = session.query(Shelters).all()
            print(shelters)
            session.close()
            return render_template('resources.html', shelters = shelters)
    except Exception as e:
        print(e)
        flash("Something went wrong. Please try again.")
        return redirect(url_for('index'))

@app.route('/dog')
@app.route('/dog/<int:id>', methods=['GET', 'POST'])
@login_required
def dog(id):
    try:
        isAdmin = False
        if current_user.email in admins:
            isAdmin = True
        if request.method == 'POST' and isAdmin == True:
           with app.app_context():
               session = Session(db.engine)  # TODO: don't create a new session, but reuse a globl session var
               dog = session.query(Dogs).filter_by(ID=id)
               dog.update({"Name":request.form['Name'], "Sex":request.form['Sex'], "DateofBirth":request.form['DateofBirth']})
               
               needs = session.query(AdoptionNeeds).filter_by(ID=id)
               needs.update({ "Housetrained":request.form['Housetrained'], "Kids":request.form['Kids'], "Otherdogs-Play":request.form['Otherdogs-Play']})

               db.session.commit()
               session.close()
               return redirect(url_for('dog', id=id))
        else:
            with app.app_context():
                session = Session(db.engine)
                dog = session.query(Dogs).filter_by(ID=id).first()
                needs = session.query(AdoptionNeeds).filter_by(ID=id).first()
                session.close()
                if dog:
                    return render_template('dog.html', id = id, dog = dog, needs = needs, isAdmin = isAdmin)
                else:
                    flash("This dog does not exist.")
                    return redirect(url_for('home'))
    except Exception as e:
        print(e)
        flash("Something went wrong. Please try again.")
        return redirect(url_for('home'))
@app.route('/community')
@login_required
def community():
    try:
        return render_template('community.html')
    except Exception as e:
        print(e)
        flash("Something went wrong. Please try again.")
        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
# Upload images and insert image URLs in database
# Finish adding all relevant fields in Dog from DogMedical and DogAdoption
# Adding Shelters to Resources or planning what to write on the page
# Seperate Sex and Breed in database