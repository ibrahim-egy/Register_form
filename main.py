import sqlite3
from flask import Flask, render_template, request, url_for, redirect, flash, get_flashed_messages
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from wtforms_validators import Alpha
from flask_bootstrap import Bootstrap
import os

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Users.db'
db = SQLAlchemy(app)
Bootstrap(app)


# User DB tabel
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    fname = db.Column(db.String(50))
    lname = db.Column(db.String(50))


# db.create_all()

class RegisterForm(FlaskForm):
    user_name = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(),
                                                     Length(min=8,
                                                            max=25,
                                                            message="password must be 8 length and have an "
                                                                    "upper & lowercase characters"),
                                                     EqualTo('confirm',
                                                             message='Passwords must match')])
    confirm = PasswordField("Confirm Password")
    email = StringField("Email", validators=[DataRequired(), Email()])
    first_name = StringField("First name", validators=[DataRequired(),
                                                       Alpha(message="First Name Must contain "
                                                                     "characters only!")])
    last_name = StringField("Last name", validators=[DataRequired(),
                                                     Alpha(message="Last Name Must contain "
                                                                   "characters only!")])
    submit = SubmitField("Sign me up!")


@app.route('/', methods=["GET", "POST"])
def home():
    form = RegisterForm()
    errors = get_flashed_messages()
    if form.validate_on_submit():
        if User.query.filter_by(email=request.form.get('email')).first():
            flash("you've already signed up with that email!")
            return redirect(url_for('home'))
        new_user = User()
        if User.query.filter_by(username=request.form['user_name']).first():
            flash("Username already exist!")
            return redirect(url_for('home'))
        new_user.username = request.form['user_name']
        new_user.password = request.form["password"]
        new_user.email = request.form['email']
        new_user.fname = request.form['first_name']
        new_user.lname = request.form['last_name']
        db.session.add(new_user)
        db.session.commit()
        flash("Data Saved Successfully.")
        return redirect(url_for('home'))
    return render_template("index.html", form=form, errors=errors)


if __name__ == '__main__':
    app.run(debug=True)
