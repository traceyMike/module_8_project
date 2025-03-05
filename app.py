# hold all application data - python code

# Importing the modules
# Render_template - renders the HTML and request handles form data
# Redirect and url for direct users to route in the website navigation
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# create new flask app
app = Flask(__name__) # creates new flask app then configure sqlite db after

# Configure SQLite db
app.config('SQLALCHEMY_DATABASE_URI') = 'sqlite:///todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app) # db allows us to connect to db, get model, columns, etc.

#Define Todo Model Class(models a to do list item that is stored in the dattabase)
# Define the columns(attributes) for the class
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True) # id column is int
    title = db.Column(db.String(100), nullable = False) # title column is string
    done = db.Column(db.Boolean, default = False) # done column is a boolean
    created_at = db.Column(db.DateTime, default = datetime.utcnow) # created_at column contains current time

    # Add the repr method - return string representing the object
    def __repr__(self):
        return f'<todo id="{self.id}" title="{self.title}" done="{self.done}" created_at="{self.created_at}">'
    
# Create the database and table to hold the "To Do's"
with app.app_context():
    db.create_all() # create_all() creates table in db that copies our table in todo list - columns will match exactly

# now we have database, table, and class

# Create a home route that displays the todo list
@app.route('/') # / indicates default url for that domain (GET the default domain)
def index():
    # grab all todo list items, put them in result set in desc order by the date
    todos = Todo.query.order_by(Todo.created_at.desc()).all() # create todos and populate by querying the db
    # return a value displayed in users browser
    return render_template('index.html', todos=todos) # apply index.html code to result set of todos

# Create a route for adding a new To Do item to the database
@app.route('/add', methods=['GET'])
def add(): 
    # get the title of the todo item from the HTML form on the webpage
    title = request.form.get('title')

    # if the title is not null, then create new todo list item record in db
    # Else redirect the user to the index page(home page)
    if title:
        new_todo = Todo(title=title)
        db.session.add(new_todo)
        db.session.commit() # call commit when adding to db
    return redirect(url_for('index')) # return user to the home page - if title entered or not

# Create route for marking a To Do item as done
@app.route('/toggle/<int:todo_id>')
def toggle(todo_id):
    # Update the database record and mark the todo list item as done 
    # (if something goes wrong and to do list item does not exist display a 404 error)
    todo = Todo.query.get_or_404(todo_id) # get record for todo or if no record in db show 404
    # Mark the to do list item as done in the database
    todo.done = not todo.done
    db.session.commit()
    return redirect(url_for('index'))

# Create route to delete the to do item
@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    # Check if a db record exists with the ID number
    # and if no matching record - show a 404 error
    todo = Todo.query.get_or_404(todo_id)
    # Delete the record in the db for the todo item
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))

# Start the Flask app in debug mode
# Flask provides a debugger that shows a stack trace if error occurs
# debug mode also reloads the page automatically when you make a change
# when you change code you do not need to restart the server
# save time when making little changes to html to see how it looks
# makes process much faster

# add main method
if __name__ == '__main__':
    app.run(debug=True) # call run method on application