#make sign up page
#finish building out home page
#come up with classes for the dogs

from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_login import login_required, login_manager, login_user, logout_user, current_user, LoginManager, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from amazons3 import image_urls

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DogShelter2.db'
app.config['FLASK_DEBUG']=1
app.secret_key = "1234567"  # TODO: use os.getenv()

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
POSTS_PER_PAGE = 21

admins = ['ishan.kunada@gmail.com', 'admin@gmail.com', 'admin2@gmail.com', 'csumani@yahoo.com', 'mehanni@gmail.com']

class Adopterinfo(db.Model):
    __tablename__ = 'AdopterInfo'
    ID = db.Column(db.Integer, primary_key=True)
    TagNumber = db.Column(db.String(128))
    Name = db.Column(db.String(128))
    Adopter = db.Column(db.String(128))
    Phone = db.Column(db.String(128))
    Email = db.Column(db.String(128))
    AdoptionDate = db.Column(db.String(128))
    Contract = db.Column(db.String(128))
    PaymentConfirmation = db.Column(db.String(128))
    CheckNumber = db.Column(db.String(128))
    Email2 = db.Column(db.String(128))
    Address = db.Column(db.String(128))
    City = db.Column(db.String(128))
    St = db.Column(db.String(128))
    Zip = db.Column(db.String(128))
    AdoptercellPhone = db.Column(db.String(128))
    AdopterHomePhone = db.Column(db.String(128))
    AdopterWorkphone = db.Column(db.String(128))
    Comments = db.Column(db.String(128))
    Transferred = db.Column(db.String(128))
    FileLocation = db.Column(db.String(128))

class Dogadoptionneeds(db.Model):
    __tablename__ = 'DogAdoptionNeeds'
    ID = db.Column(db.Integer, primary_key=True)
    TagNumber = db.Column(db.String(128))
    Name = db.Column(db.String(128))
    OtherdogsPlay = db.Column(db.String(128))
    OtherdogsParalelllive = db.Column(db.String(128))
    Cats = db.Column(db.String(128))
    Kids = db.Column(db.String(128))
    Housetrained = db.Column(db.String(128))
    Cratetrained = db.Column(db.String(128))
    leashwalk = db.Column(db.String(128))
    Doorescape = db.Column(db.String(128))
    Digger = db.Column(db.String(128))
    Vocal = db.Column(db.String(128))
    FireworksFear = db.Column(db.String(128))
    Specialneeds = db.Column(db.String(128))
    Notes = db.Column(db.String(128))

class Dogmedical(db.Model):
    __tablename__ = 'DogMedical'
    ID = db.Column(db.Integer, primary_key=True)
    TagNumber = db.Column(db.String(128))
    Dated = db.Column(db.String(128))
    Name = db.Column(db.String(128))
    Sex = db.Column(db.String(128))
    Breed = db.Column(db.String(128))
    picture = db.Column(db.String(128))
    DateofBirth = db.Column(db.String(128))
    Status = db.Column(db.String(128))
    Source = db.Column(db.String(128))
    MicrochipNumber = db.Column(db.String(128))
    Type = db.Column(db.String(128))
    VaccinationDate = db.Column(db.String(128))
    VaccPaperworkReceived = db.Column(db.String(128))
    Veterinarian = db.Column(db.String(128))
    SizeAndLbs = db.Column(db.String(128))
    SpayAndNeuterDate = db.Column(db.String(128))
    RabiesTagNumber = db.Column(db.String(128))
    HeartWormTestDate = db.Column(db.String(128))
    HeartwormTestResults = db.Column(db.String(128))
    Heartwormprev = db.Column(db.String(128))
    medicalissues = db.Column(db.String(128))
    Foster = db.Column(db.String(128))
    Phone = db.Column(db.String(128))
    Email = db.Column(db.String(128))

class Fosterinfo(db.Model):
    __tablename__ = 'FosterInfo'
    ID = db.Column(db.Integer, primary_key=True)
    TagNumber = db.Column(db.String(128))
    Name = db.Column(db.String(128))
    Foster = db.Column(db.String(128))
    Phone = db.Column(db.String(128))
    Email = db.Column(db.String(128))
    Fosterspets = db.Column(db.String(128))

class Shelters(db.Model):
    __tablename__ = 'Shelters'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(128))
    name = db.Column(db.String(128))
    description = db.Column(db.String(128))

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


@login_manager.user_loader
def load_user(user_id):
  """
  Loads a user from the database based on the user_id provided.
  Returns the User object corresponding to the user_id.
  """
  user = Users.query.get(int(user_id))
  session["isAdmin"] = user.email in admins
  return user

@app.route('/')
@login_required
def index():
    return render_template("index.html")

@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    session['images'] = image_urls
    with app.app_context():

        if request.method == 'POST' :
            try:
                search = request.form.get('search')
                dogs = db.session.query(Dogmedical).filter(Dogmedical.Name.ilike(f"%{search}%")).order_by(Dogmedical.Name).all()
                return render_template("home.html", dogs = dogs)
            except Exception as e:
                print(e)
                flash("Something went wrong. Please try again.")
                return redirect(url_for('home', dogs = dogs))
        else:
            query = db.session.query(Dogmedical).order_by(Dogmedical.Name)
            page = request.args.get('page', 1, type=int)
            dogs = db.paginate(query, page=page, per_page=POSTS_PER_PAGE, error_out=False)
            next_url = url_for('home', page=dogs.next_num) if dogs.has_next else None
            prev_url = url_for('home', page=dogs.prev_num) if dogs.has_prev else None
            return render_template("home.html", dogs = dogs.items, next_url = next_url, prev_url = prev_url)


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
    session["isAdmin"] = False
    return redirect(url_for('login'))

@app.route('/resources')
def resources():
    try:
        shelters = db.session.query(Shelters).all()
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
        dog = Dogmedical.query.get(id)
        needs = Dogadoptionneeds.query.get(id)

        if not dog:
            flash("This dog does not exist.")
            return redirect(url_for('home'))

        if request.method == 'POST' and session["isAdmin"]:
            for key, value in request.form.items():
                if hasattr(dog, key) and getattr(dog, key) != value:
                    setattr(dog, key, value)
                elif hasattr(needs, key) and getattr(needs, key) != value:
                    setattr(needs, key, value)

            db.session.commit()
            flash("Changes saved.")
            return redirect(url_for('dog', id=id))
        return render_template('dog.html', id=id, dog=dog, needs=needs, isAdmin=session["isAdmin"])
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

@app.route('/newdog', methods=['GET', 'POST'])
@login_required
def newdog():
    try:
        if request.method == 'POST' and session["isAdmin"]:
            new_dog_adopterinfo = Adopterinfo()
            new_dog_medical = Dogmedical()
            new_dog_adoptionneeds = Dogadoptionneeds()
            for key, value in request.form.items():
                if key=="Name": 
                    value = value.title() 

                if hasattr(Dogmedical, key):
                    setattr(new_dog_medical, key, value)
                if hasattr(Dogadoptionneeds, key):
                    setattr(new_dog_adoptionneeds, key, value)
                if hasattr(Adopterinfo, key):
                    setattr(new_dog_adopterinfo, key, value)
            
            db.session.add(new_dog_medical)
            db.session.add(new_dog_adoptionneeds)
            db.session.add(new_dog_adopterinfo)
            db.session.commit()
            flash("New dog added")
            
            return redirect(url_for('home'))
        else:
            return render_template('newdog.html')
    except Exception as e:
        print(e)
        flash("Something went wrong. Please try again.")
        return redirect(url_for('newdog.html'))


if __name__ == '__main__':
    app.run(debug=True)
# Upload images and insert image URLs in database
# Finish adding all relevant fields in Dog from DogMedical and DogAdoption
# Adding Shelters to Resources or planning what to write on the page