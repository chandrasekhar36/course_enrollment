
from application import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Document):
    user_id=db.IntField(unique=True)
    first_name=db.StringField(max_length=50)
    last_name=db.StringField(max_length=50)
    email=db.StringField(max_length=30)
    password=db.StringField(max_length=300)
    def set_password(self,password):
        self.password=generate_password_hash(password)
    def get_password(self,password):
        return check_password_hash(self.password,password)
class Course(db.Document):
    courseID=db.StringField(unique=True,max_length=10)
    title=db.StringField(max_length=100)
    description=db.StringField(max_length=250)
    credits=db.IntField(max_length=30)
    term=db.StringField(max_length=30)

class Enrollment(db.Document):
    user_id=db.IntField()
    courseID=db.StringField(max_length=10)
