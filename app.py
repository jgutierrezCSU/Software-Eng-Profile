from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app=Flask(__name__)
#config database location using SQLITE relative path
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
db=SQLAlchemy(app) #initialize database

#create a model
class Todo(db.Model):
    # creates ID for each entry
    id= db.Column(db.Integer,primary_key=True)
    content= db.Column(db.String(150),nullable=False)
    completed= db.Column(db.Integer)
    # set time automatically
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')

if __name__ =="__main__":
    app.run(debug=True)