from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, current_user, logout_user, login_required

from wtform_fields import *
from models import *

app = Flask(__name__)
app.secret_key="nfjasfbasfbasbfhasbjh"
app.config['WTF_CSRF_SECRET_KEY'] = "b'f\xfa\x8b{X\x8b\x9eM\x83l\x19\xad\x84\x08\xaa"


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login = LoginManager(app)
login.init_app(app)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

#To create the tables at the start of the application
@app.before_first_request
def create_tables():
    db.create_all()


#  Register user
# This is the endpoint when anyone visits our website and user have to provide unique username, password and confirmed password. after
#sucessfully providing it creates our User object in database and redirects user to login page
# URL : http://localhost:5000/
#
@app.route("/", methods=['GET', 'POST'])
def index():

    reg_form = RegistrationForm(request.form)

    # Update database if validation success
    if request.method=='POST' and reg_form.validate() :
        username = reg_form.username.data
        password = reg_form.password.data

        # Hash password
        hashed_pswd = pbkdf2_sha256.hash(password)

        # Add username & hashed password to DB
        user = User(username=username, hashed_pswd=hashed_pswd)
        print(user)
        db.session.add(user)
        db.session.commit()

        flash('Registered successfully. Please login.', 'success')
        return redirect(url_for('login'))

    return render_template("index.html", form=reg_form)



#  user login
#URL : http://localhost:5000/login
# When user provides the correct username and password it will redirect it the to-do-app page and if any of the username or password is
# in-correct it will redirect to same page with appropriate error message
@app.route("/login", methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    # Allow login if validation success
    print("out of if")
    if login_form.validate():
        print("inside of if")
        user_object = User.query.filter_by(username=login_form.username.data).first()
        print(user_object)
        login_user(user_object)
        return redirect(url_for("home"))

    return render_template("login.html", form=login_form)

# user logout
#To access this user need to be logged in and after logout it will redirect to login page
# URL : http://localhost:5000/logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

#Home page
# It provides the list of the all TO-DO-LIST items and to enter the new item
# URL : http://localhost:5000/base
@app.route("/base")
@login_required
def home():
    #todo_list = Todo.query.filter_by(username=current_user.username)
    search_filter = request.args.get('se') 
    print(search_filter)
    if search_filter:
        todo_list=Todo.query.filter(Todo.id.contains(search_filter) | Todo.title.contains(search_filter))
    else:
        todo_list=Todo.query.filter_by(username=current_user.username)
    return render_template("base.html", todo_list=todo_list)


# adding the list item
# requires the title,complete(status of item) and username(who created the item), using this data it will create the object and save in the database
# URL : http://localhost:5000/add
@app.route("/add", methods=["POST"])
@login_required
def add():
    title = request.form.get("title")
    new_todo = Todo(title=title, complete=False,username=current_user.username)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("home"))

# updating the list item
# This will change the status of the item from complete to not complete or vice versa. You need id of the task of which you need to change the status
# URL : http://localhost:5000/update/<id>
#sample : http://localhost:5000/update/2
@app.route("/update/<int:todo_id>")
@login_required
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("home"))

# deleting the list item
# This will delete the item from the database. You need id of the task of which you need to be deleted
# URL : http://localhost:5000/delete/<id>
#sample : http://localhost:5000/update/1
@app.route("/delete/<int:todo_id>")
@login_required
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == "__main__":
    #db.create_all()
    create_tables()
    app.run(debug=True)