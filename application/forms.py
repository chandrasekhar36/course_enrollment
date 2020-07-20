from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError,Email
from application.models import User

class LoginForm(FlaskForm):
    email=StringField("email",validators=[DataRequired(),Length(min=3,max=30)],description="Enter Email")
    #[validators.Length(min=4,max=25),validators.DataRequired])
    password=PasswordField("password", validators=[DataRequired(),Length(min=5,max=30)],description="Enter Password")
    remember_me=BooleanField("Rember Me")
    submit =SubmitField("Login")

class RegisterForm(FlaskForm):
    first_name=StringField("First Name",validators=[DataRequired()])
    last_name=StringField("Last Name",validators=[DataRequired()])
    email=StringField("Email",validators=[DataRequired(),Email("Please Enter Valid Email Address")])
    password=PasswordField("Password",validators=[DataRequired()])
    password_confirm=PasswordField("Confirm Password",validators=[DataRequired(),EqualTo("password","Password Mismatch")])
    submit =SubmitField("Signup")

    def validate_email(self,email):
        user=User.objects(email=email.data).first()
        if user:
            raise ValidationError("Email already in use! choose other one")
