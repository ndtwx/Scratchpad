
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import login_user, LoginManager, UserMixin, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

app = Flask(__name__)
app.config["DEBUG"] = True

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username = "woshiiandy",
    password = "Wanttoberudess",
    hostname = "woshiiandy.mysql.pythonanywhere-services.com",
    databasename = "woshiiandy$comments",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.secret_key = "i have no idea what is going on but i just continue"
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


    def get_id(self):
        return self.username

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(username=user_id).first()

class Comment(db.Model):

    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(4096))
    posted = db.Column(db.DateTime, default=datetime.now)
    commenter_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    commenter = db.relationship('User', foreign_keys=commenter_id)

#Specifies that the following function defines the view for the “/” URL, and that it accepts both “GET” and “POST” requests.
@app.route("/", methods=["GET", "POST"])
def index():
    #If the request we’re currently processing is a “GET” one, the viewer just wants to see the page, so we render the template. We’ve added an extra parameter to the call to render_template – the comments=comments bit. This means that the list of comments that we’ve defined as a variable further up will be available inside our template; we’ll update that to use the list in a moment.
    #If the request isn’t a “GET” (and so, we know it’s a “POST” – someone’s clicked the “Post comment” button) then the next bit is executed:
    if request.method == "GET":
        return render_template("main_page.html", comments=Comment.query.all())

    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    #This extracts the stuff that was typed into the textarea in the page from the browser’s request; we know it’s in a thing called contents because that was the name we gave the textarea in the template:
    #<textarea class="form-control" name="contents" placeholder="Enter a comment"></textarea>
    comment = Comment(content=request.form["contents"], commenter=current_user)
    db.session.add(comment)
    db.session.commit()

    #Once we’ve extracted the comment contents from the request, we add it to the list. Finally, once that’s been stored, we send a message back to the browser saying “Please request this page again, this time using a ‘GET’ method”, so that the user can see the results of their post:
    return redirect(url_for('index'))

@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login_page.html", error=False)

    user = load_user(request.form["username"])
    if user is None:
        return render_template("login_page.html", error=True)

    if not user.check_password(request.form["password"]):
        return render_template("login_page.html", error=True)

    login_user(user)
    return redirect(url_for('index'))

@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
