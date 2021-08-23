#library
from flask import Flask,render_template,request,flash,url_for,redirect
from flask_sqlalchemy import SQLAlchemy
import logging


app = Flask(__name__)
app.config['SECRECT_KEY'] = 'XYZABC'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
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
    return render_template('todolist.html',flag = True,items = create_list.query.all() )

@app.route('/add',methods = ['GET','POST'])
def add():
    if request.method == 'POST':
        if not request.form['task']:
            flash("Please Enter Work Name")
        else:
            add_item = create_list(list_text=request.form['task'],list_user_id=1)
            db.session.add(add_item)
            db.session.commit()
        return redirect('/')
    else:
        logging.error("INVALID REQUEST")
        


@app.route('/remove',methods = ['GET','POST'])
def remove():
    create_list.query.filter_by(list_id=request.args.get('id')).delete()
    db.session.commit()
    return redirect('/')


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
    

