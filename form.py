from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, URLField, DecimalField, PasswordField
from wtforms.validators import DataRequired, URL, NumberRange


class CafeForm(FlaskForm):
    name = StringField('Cafe name', validators=[DataRequired()])
    map_url = URLField('Cafe Location on Google Map (URL)', validators=[DataRequired(), URL()])
    img_url = URLField('Cafe Image (URL)', validators=[DataRequired(), URL()])
    location = StringField('Cafe Location', validators=[DataRequired()])
    has_sockets = SelectField('Cafe has sockets?', choices=[(True,'True'), (False, 'False')], coerce=bool)
    has_toilet = SelectField('Cafe has toilet?', choices=[(True,'True'), (False, 'False')], coerce=bool)
    has_wifi = SelectField('Cafe has wifi?', choices=[(True,'True'), (False, 'False')], coerce=bool)
    can_take_calls = SelectField('Cafe can take calls?', choices=[(True,'True'), (False, 'False')], coerce=bool)
    seats = StringField('Number of Cafe Seat', validators=[DataRequired()])
    coffee_price = DecimalField('Coffee Price (dong)', validators=[DataRequired(), NumberRange(min=0, max=100)])
    submit = SubmitField('Submit')

class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField("Sign Up")

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log in')
