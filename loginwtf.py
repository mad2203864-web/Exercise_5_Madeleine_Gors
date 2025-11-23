from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, RadioField, SelectField
from wtforms.validators import DataRequired, Email, Length, NumberRange, Regexp, URL, InputRequired

class LoginWTF(FlaskForm):
    user_name = StringField('User Name:', validators=[DataRequired()])
    pass_word = PasswordField('Password:', validators=[DataRequired()])

    myusertypes = [(0,'Guest'),(1,'Basic'),(2,'Moderator'),(3,'Administrator')]
    user_type = RadioField('usertype', choices=myusertypes,validators=[DataRequired()])

    user_email = StringField('Email Address', validators=[InputRequired("Please enter an Email Address"),Email("This field requires a valid Email address")])

    myoptions = [(None, "Choose your pet"), ('Dog','dog'),('Cat','cat'),
                 ('carpet shark','ferret'),('werewolf','Doggie!')]
    pet_choice = SelectField("PetChoice", choices=myoptions,validators=[DataRequired()] )
