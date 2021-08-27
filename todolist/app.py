#library
from flask import Flask,render_template,request,flash,url_for,redirect,session
from flask_sqlalchemy import SQLAlchemy
import logging
import pymysql
import random
import string

app = Flask(__name__,template_folder='templates')
app.secret_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost:3306/todolist'
db = SQLAlchemy(app)


class create_user(db.Model):
    user_id = db.Column(db.Integer(),primary_key = True,autoincrement = True)
    user_name = db.Column(db.String(40),nullable = False)
    user_email = db.Column(db.String(40),nullable = False)
    user_password = db.Column(db.String(64),nullable = False)

class create_list(db.Model):
    list_id = db.Column(db.Integer(),primary_key = True,autoincrement = True)
    list_text = db.Column(db.Text(),nullable = False)
    list_user_id = db.Column(db.Integer())#,db.ForeignKey('create_user.user_id'))

@app.route('/')
def index():
    try:
        return render_template('index.html',flag = True,items = create_list.query.filter_by(list_user_id =session['user_id']).all() )
    except KeyError:
        return render_template('index.html',flag = False)

@app.route('/add',methods = ['GET','POST'])
def add():
    if request.method == 'POST':
        if not request.form['task']:
            flash("Please Enter Work Name")
        else:
            if session['user_id']:
                add_item = create_list(list_text=request.form['task'],list_user_id=session['user_id'])
                db.session.add(add_item)
                db.session.commit()
                flash("Work added successfully")
            else:
                flash("Please login to enter data")
        return redirect('/')
    else:
        logging.error("INVALID REQUEST")
        


@app.route('/remove',methods = ['GET','POST'])
def remove():
    create_list.query.filter_by(list_id=request.args.get('id')).delete()
    db.session.commit()
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

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
    

