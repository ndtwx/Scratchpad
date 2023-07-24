
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

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

class Comment(db.Model):

    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(4096))

comments = []

#Specifies that the following function defines the view for the “/” URL, and that it accepts both “GET” and “POST” requests.
@app.route("/", methods=["GET", "POST"])
def index():
    #If the request we’re currently processing is a “GET” one, the viewer just wants to see the page, so we render the template. We’ve added an extra parameter to the call to render_template – the comments=comments bit. This means that the list of comments that we’ve defined as a variable further up will be available inside our template; we’ll update that to use the list in a moment.
    #If the request isn’t a “GET” (and so, we know it’s a “POST” – someone’s clicked the “Post comment” button) then the next bit is executed:
    if request.method == "GET":
        return render_template("main_page.html", comments=comments)
    #This extracts the stuff that was typed into the textarea in the page from the browser’s request; we know it’s in a thing called contents because that was the name we gave the textarea in the template:
    #<textarea class="form-control" name="contents" placeholder="Enter a comment"></textarea>
    comments.append(request.form["contents"])
    #Once we’ve extracted the comment contents from the request, we add it to the list. Finally, once that’s been stored, we send a message back to the browser saying “Please request this page again, this time using a ‘GET’ method”, so that the user can see the results of their post:
    return redirect(url_for('index'))
