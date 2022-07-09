
import email
from flask import Flask, render_template, abort, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, login_user, login_required, logout_user, current_user ,UserMixin


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root@localhost/app"
app.config['SECRET_KEY'] = 'mambacita'

db = SQLAlchemy(app)

Admin = Admin(app)

LoginManager = LoginManager()
LoginManager.init_app(app)
LoginManager.login_view = 'login'




class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))


# db.create_all()

#routes

@LoginManager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/process', methods=['POST'])
def process():
        email = request.form['email']
        password = request.form['password']
        #return("email: " + email + " password: " + password)
        email = User.query.filter_by(email=email).first()
        if email == email:
            if email.password == password:
                login_user(email)
                return redirect(url_for('index'))
            else:
                flash('Invalid password')
                return redirect(url_for('login'))
     
            


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        
        #grab the data from the form
        
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        #save user data to database
        
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        db.session.close()
        flash('You were successfully registered and can now login')
        return redirect(url_for('login'))
    else:
        flash('registarion failed')
        return render_template('register.html', failed=True)
    


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('You were logged out')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
    # app.run(host='
