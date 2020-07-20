from application import app,db,api
from application.models import User,Course,Enrollment
from flask import render_template,request,Response,redirect, flash, session, url_for,jsonify
from application.forms import LoginForm,RegisterForm
import json
from flask_restplus import Resource


##########API################
@api.route('/api')
class GetAll(Resource):
    def get(self):
        return jsonify(User.objects.all())

    def post(self):
        data=api.payload
        user=User(user_id=data['user_id'],first_name=data['first_name'],last_name=data['last_name'],email=data['email'])
        user.set_password(data['password'])
        user.save()
        return "User_id "+str(data['user_id'])+" added succeesfully as per your request"



@api.route('/api/<id>')
class GetSelected(Resource):
    def get(self,id):
        return jsonify(User.objects(user_id=id))

    def put(self,id):
        data=api.payload
        user=User.objects(user_id=id).update(**data)
        return str(id)+" updated  succeesfully As per your request"

    def delete(self,id):
        User.objects(user_id=id).delete()
        return "user deleted"




#############API##############
@app.route('/')
@app.route('/home')
def index():
    if session.get('user_id')==None:
        home=False
    else:
        home=True
    return render_template('index.html',login=home)#"<h1>hey!, how do you do</h1>"


@app.route('/courses/')
@app.route('/courses/<term>')
def courses(term=None):
    if session.get('user_id')==None:
        return redirect(url_for('login'))
    if term==None:
        term="Spring 2020"
    courseData=Course.objects.order_by("courseID")
    return render_template('courses.html',term=term,courseData=courseData,course=True)

@app.route('/login',methods=['GET','POST'])
def login():
    if session.get('user_id'):
        return redirect('/')
    form=LoginForm()
    if form.validate_on_submit():
        mail=form.email.data
        password=request.form.get('password')
        user=User.objects(email=mail).first()
        if user and user.get_password(password):
            flash(f'hey {user.first_name}, Welcome to your dashboard','success')
            session['user_id']=user.user_id
            session['user_name']=user.first_name
            return redirect('/home')
        else:
            flash("Sorry! Something went wrong","danger")
    return render_template('login.html',title="Login",form=form,login=True)

@app.route('/register',methods=['GET','POST'])
def register():
    if session.get('user_id'):
        return redirect('/')
    form=RegisterForm()
    if form.validate_on_submit():
        id=User.objects.count()+1
        first_name=form.first_name.data
        last_name=form.last_name.data
        email=form.email.data
        password=form.password.data
        user=User(user_id=id,first_name=first_name,last_name=last_name,email=email)
        user.set_password(password)
        user.save()
        flash("Registered Succesfully",'success')
        return redirect('/home')
    return render_template('register.html',register=True,title="Register",form=form)

@app.route('/enroll',methods=['POST','GET'])
def enroll():
    print(session.keys(),session.values())
    if session.get('user_id')==None:
        return redirect(url_for('login'))
    current_user=session['user_id']
    user_name=session.get('user_name')
    title=request.form.get('title')
    id=request.form.get('id')
    print(id,current_user)
    term=request.form.get('term')
    data=[]
    if id:
        classes=Enrollment.objects(user_id=current_user,courseID=id).first()
        if classes:
            #stopping duplicate enrollings
            flash(f'Hey {user_name}, you already enrolled in {title}','danger')
            return redirect(url_for('courses'))
    Enrollment(user_id=current_user,courseID=id).save()
        #classes=Enrollment.objects(user_id=user).all()
    data=list(User.objects.aggregate(*[
    {
        '$lookup': {
            'from': 'enrollment',
            'localField': 'user_id',
            'foreignField': 'user_id',
            'as': 'r1'
        }
    }, {
        '$unwind': {
            'path': '$r1',
            'includeArrayIndex': 'string',
            'preserveNullAndEmptyArrays': False
        }
    }, {
        '$lookup': {
            'from': 'course',
            'localField': 'r1.courseID',
            'foreignField': 'courseID',
            'as': 'r2'
        }
    }, {
        '$unwind': {
            'path': '$r2',
            'preserveNullAndEmptyArrays': False
        }
    }, {
        '$match': {
            'user_id': current_user
        }
    }, {
        '$sort': {
            'courseID': 1
        }
    }
]))
    return render_template('enroll.html',title="Registered Courses",enroll=True,courseData=data)

@app.route('/api/')
@app.route('/api/<id>')
def get_api(id=None):
    if id==None:
        data=courseData
    else:
        data=courseData[int(id)]
    return Response(json.dumps(data),mimetype='application/json')

@app.route('/logout')
def logout():
    session['user_name']=None
    session['user_id']=None
    return redirect(url_for('index'))

@app.route('/user')
def user():
    users=User.objects.all()
    return render_template('user.html',users=users)
