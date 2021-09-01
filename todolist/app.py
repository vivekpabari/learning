#library
from flask import Flask,render_template,request,flash,url_for,redirect,session
from flask_sqlalchemy import SQLAlchemy
import logging
import pymysql
import random
import string
import json
from flask_mail import Mail,Message
from flask_restful import Api,Resource


app = Flask(__name__,template_folder='templates')
app.secret_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost:3306/todolist'
db = SQLAlchemy(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'vivek.v.pabari@gmail.com'
app.config['MAIL_PASSWORD'] = password
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
api = Api(app)


def Send_mail(email):
    print(email)
    msg = Message('Password reset',sender ='vivek.v.pabari@gmail.com',recipients = [email])
    msg.body = str(random.randrange(1000,9999))
    mail.send(msg)

class create_user(db.Model):
    user_id = db.Column(db.Integer(),primary_key = True,autoincrement = True)
    user_name = db.Column(db.String(40),nullable = False)
    user_email = db.Column(db.String(40),nullable = False)
    user_password = db.Column(db.String(64),nullable = False)

class create_list(db.Model):
    list_id = db.Column(db.Integer(),primary_key = True,autoincrement = True)
    list_text = db.Column(db.Text(),nullable = False)
    list_user_id = db.Column(db.Integer())#,db.ForeignKey('create_user.user_id'))
    
class user_list(Resource):
    def get(self):
        d = {
            "name":"vivek",
            "date":"01/09/2020"
            }
        return json.dumps(d)

api.add_resource(user_list,'/user')

@app.route('/')
def index():
    try:
        return render_template('index.html',flag = True,items = create_list.query.filter_by(list_user_id =session['user_id']).all() )
    except KeyError:
        return render_template('index.html',flag = False)

@app.route('/increament/<int:number>')
def increament(number):
    return str(number+10)

@app.route('/add',methods = ['GET','POST'])
def add():
    if request.method == 'POST':
        if not request.form['task']:
            flash("Please Enter Work Name")
        else:
            try:
                add_item = create_list(list_text=request.form['task'],list_user_id=session['user_id'])
                db.session.add(add_item)
                db.session.commit()
                flash("Work added successfully")
            except:
                flash("Please login to enter data")
        return redirect('/')
    else:
        logging.error("INVALID REQUEST")
        


@app.route('/remove',methods = ['GET','POST'])
def remove():
    create_list.query.filter_by(list_id=request.args.get('id')).delete()
    db.session.commit()
    flash("work removed sucessfully")
    return redirect('/')


@app.route('/user/login')
def login():
    logging.debug("inside login module")
    return render_template('login.html')

@app.route('/user/login_verification',methods = ['GET','POST'])
def login_verification():
    if request.method == 'POST':
        if not request.form['email'] or not request.form['password']:
            flash("ENTER ALL FIELD")
        else:
            user = create_user.query.filter_by(user_email=request.form['email']).first()
            if user==None or user.user_password != request.form['password']:
                flash("email or password is invalid")
                return redirect('/user/login')
            else:
                #start session
                flash("Login is successful")
                session['user_id'] = user.user_id
                session['user_name'] = user.user_name
                return redirect('/')


@app.route('/user/signup')
def signup():
    return render_template('signup.html')

@app.route('/user/signup_verification',methods = ['GET','POST'])
def signup_verification():
    if request.method == 'POST':
        if not request.form['email'] or not request.form['password'] or not request.form['name']:
            flash("Enter All Field",category='signup_field_empty')
        else:
            user = create_user(user_name=request.form['name'],user_email=request.form['email'],user_password = request.form['password'])
            db.session.add(user)
            db.session.commit()
            session['user_id'] = user.user_id
            session['user_name'] = user.user_name
            flash("Account Create Successfully",)
    return redirect('/')
@app.route('/user/logout')
def logout():
    session.clear()
    flash("Logout successfully")
    return redirect('/')

@app.route('/user/forget_password')
def forget_password():
    return render_template('forget.html')

@app.route('/user/send_forget_password_otp',methods =  ['POST'])
def send_forget_password_otp():
    if request.method == 'POST':
        if not request.form['email']:
            return redirect('/user/forget_password')
        else:
            Send_mail(request.form['email'])
            return render_template('set_password.html')
    else:
        return redirect('/user/forget_password')
@app.route('/user/password_set',methods = ['POST','GET'])
def password_set():
    if request.method == 'POST':
        if not request.form['otp'] or not request.form['password'] or not request.form['password_confirm']:
            return render_template('set_password.html')
        else:
            user = create_user.query.filter_by(user_email=request.form['email']).first()
            user.user_password = request.form['password']
            db.session.commit()

            return redirect('/')
    else:
        return render_template('set_password.html')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
    

