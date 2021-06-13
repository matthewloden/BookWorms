from flask_wtf import FlaskForm
from wtforms_components import DateField, DateRange
from wtforms import StringField, BooleanField, PasswordField, SubmitField
from wtforms.validators import InputRequired, DataRequired, EqualTo, Length, Email, ValidationError
from app.DBconnect import engine, create_engine, text
from app import logging
import pandas as pd
import logging


# Validation Function:
# Unique email validator, Unique password validator, and  Unique username validator (enduser)
def uniquedata(form, field):
    with engine.connect() as conn:
        sql_query="SELECT email FROM dev.users;"  
        usrdatadf = pd.read_sql(sql_query,conn)
        usrdata = usrdatadf.to_dict('list')['email']
        if field.data in usrdata:
            logging.error("User " + str(field.data) + " already exists in database.")
            raise ValidationError("User "+ str(field.data) +" already exists in database.")
    

# Login and Registration Forms
# Login form class.
class LoginForm(FlaskForm):
    try:
        # Setting username requirements for registration form
        email = StringField('Email', validators = [InputRequired(), Email(), Length(min = 3, max = 100)])
        password = PasswordField('Password', validators = [InputRequired(), Length(min = 3, max = 30)])
        submit = SubmitField('Login')
    except Exception as e:
        logging.error(str("Error: " + str(e)))

# Registration form class.
class RegForm(FlaskForm):
    try:
        # Setting username requirements for registration form
        email = StringField('Email', validators = [InputRequired(), Email(),Length(min = 3, max = 100),uniquedata])
        name = StringField('Name', validators = [InputRequired(),Length(min = 3, max = 100)])
        age = StringField('Age', validators = [InputRequired(), Length(min = 1, max = 3)])
        password = PasswordField('Password', validators = [InputRequired(), Length(min = 3, max = 30)])
        pw_confirm = PasswordField('Re-type your password', validators = [InputRequired(), EqualTo('password', message = "Incorrect password")])
        submit = SubmitField('Sign up')
    except Exception as e:
        logging.error(str("Error: " + str(e)))





