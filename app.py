from flask import Flask, render_template, url_for, request, redirect

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__)
#config database location using SQLITE relative path
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///SummaryDB.db'
db=SQLAlchemy(app) #initialize database

#create a model
class SummaryDB(db.Model): # SummaryDB name of DB
    # creates ID for each entry
    id= db.Column(db.Integer,primary_key=True)
    title= db.Column(db.String(150),nullable=False)
    summary= db.Column(db.String(200))
    # set time automatically
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id
        
# Main entry point
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method =='POST':
        #request is equal to "name=compt_summary" from index.html name tag
        compt_summary = request.form["compt_summary"]
        #request is equal to "content_title" from index.html input tag
        compt_title = request.form["compt_title"]
        # All data added to DB needs to be in a single call, like so:
        new_post_title_summary = SummaryDB(title=compt_title,summary=compt_summary)
        
        

        try:
           
            db.session.add(new_post_title_summary)
            db.session.commit()
            return redirect('/')

        except :
            return "Issue updating your list" 
           
    else:
        # sort DB by order created and return items
        all_post= SummaryDB.query.order_by(SummaryDB.date_created).all()
        return render_template('index.html', all_post=all_post)
    
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete= SummaryDB.query.get_or_404(id)
    
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')

    except:
        return "Issue delete task"

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = SummaryDB.query.get_or_404(id)

    if request.method == 'POST':
        task.title = request.form['title']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task)



if __name__ =="__main__":
    app.run(debug=True)