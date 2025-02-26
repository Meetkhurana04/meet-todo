import os
from flask import Flask,render_template, request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.sql import func


app = Flask(__name__)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # Current directory ka path
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(BASE_DIR, 'todo.db')}"# yeh os.path hume tab jruarat hui kyuki humari todo instance ke andar bn rhi thi
app.config['SQLALCHEMY_TRACK_MODIFICATION']=False 
app.config['SQLALCHEMY_ECHO'] = True

# NECESSARY NHI TOH WARNING DEGA


db=SQLAlchemy(app) # Yeh line db object define karti hai
class Todo(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    desc=db.Column(db.String(500),nullable=False)
    date_created=db.Column(db.DateTime,default=func.now())

    def __repr__(self):
        return f"{self.sno} - {self.title} "

# jab bhi route se post ko connect krna 
# ki skoshis krte h toh method me likhna pdega ki hum kya kya use kr rhe h 
@app.route("/",methods=['GET','POST']) # yeh home page hoga
def hello_world():
    if request.method=='POST':
        title=request.form['title']
        desc = request.form['desc']

        todo =Todo(title=title,desc=desc)#instance
        db.session.add(todo)#add krega
        db.session.commit()# confirm kregaa
    alltodo=Todo.query.all() # give a list of all the databse and store in altodo named varaible
    # print("alltodo ",alltodo) 
    return render_template('index.html',alltodo=alltodo)
    #[1 - first todo , 2 - first todo , 3 - first todo , 4 - first todo , 5 - first todo ]
#endpoints khte hise
@app.route("/show")
def products():
    alltodo=Todo.query.all() # saare fucntion dikhadega
    print(alltodo) # yeh terminal me rpr fuction dikhayega
    return "<p>product page</p>"

# end pointsn

@app.route("/delete/<int:sno>",methods=['GET','POST'])
def delete(sno):
    todo=Todo.query.filter_by(sno=sno).first()
    if todo: 
      db.session.delete(todo)
      db.session.commit()
    return redirect('/')
    

@app.route("/update/<int:sno>",methods=['GET','POST'])
def update(sno):
    if request.method=='POST':
        title=request.form['title']
        desc = request.form['desc']
        todo=Todo.query.filter_by(sno=sno).first()
        todo.title=title
        todo.desc=desc 
        db.session.add(todo)#add krega
        db.session.commit()# confirm kregaa
        return redirect("/")
    todo=Todo.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=todo)

if __name__=="__main__": # yeh main file h jo call krta h jese c me htoa h app chal ja
    app.run(debug=True) # debug =true mtlb error terminal pe hi dikha 

