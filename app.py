from flask import Flask, render_template, request, redirect, url_for, abort, make_response, session
import os
from flask_wtf.csrf import CSRFProtect, CSRFError
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)


# create db  -------------------------------------------------------
file_dir = os.path.dirname("/home/ali/flask/")
goal_route = os.path.join(file_dir, "app.db")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + goal_route
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # primary_key=True
    name = db.Column(db.String(50), nullable=False)  # 50 char maximum  (unique=True)

    def __repr__(self):
        return self.name  # if i dont say User.[id, name, family, ...] return name with default


# db.create_all()

#--------------------------------------------------------------------


app.permanent_session_lifetime = timedelta(days=1)


# make directory named "uploaded_files"
path = os.path.join("uploaded_files")
os.makedirs(path, exist_ok="True")


# app.secret_key = b"\x03I\xcd\xb5\xd1\xaa\x1c\x89B\x1e\xc0\xb30ZW\t\xff\xcam\n@\x95\xb9\xd7"
app.secret_key = os.urandom(24)
csrf = CSRFProtect()
csrf.init_app(app)

@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    # return render_template('csrf_error.html', reason=e.description), 400
    return e.description, 400


@app.route("/")
def hello():
    return "hello this is index page"

# @app.route("/welcome/<name>")
# def welcome(name):
#     return "welcome %s" % (name)

# @app.route("/welcome/<string:name>")  # string can be channge with: int float path uuid
# def welcome_name(name):
#     return "welcome %s" % (name)

@app.route('/welcome/')
@app.route('/welcome/<int:id>')
def welcome(id = None): # for set default none
    massage = "The id is " + str(id)
    if id is None:
        massage = "id should not be none"
    return massage

# add html file
@app.route('/external-html')
def htmlfile():
    mylist = [1, 2, 3, 4, 5]
    return render_template("index-flask.html", neme = "ali", mylist = mylist) # it looks in templates directory by it self

@app.route("/login")
def login():
    return render_template("form.html")

# @app.route("/submit", methods=["GET"]) # default is GET
# def submit():
#     # for GET
#     # note: this request is "flask.request"!
#     email = request.args.get("email", "NO_EMAIL") # second is the defalt value
#     password = request.args.get("password", "NO_PASSWORD")

#     return render_template("submit.html", email=email, password=password)

@app.route("/submit", methods=["post"])
def submit():
    # for POST
    email = request.form.get("email", "NO_EMAIL")
    password = request.form.get("password", "NO_PASSWORD")
    
#    email = request.form["email"] # because it return us a DICTIONARY
#    password = request.form["password"]    
    return render_template("submit.html", email=email, password=password)


# if you want to use POST and GET
# @app.route("/submit", methods=["GET", "post"])
# def submit():
#     if request.method == "GET":
#         email = request.args.get("email", "NO_EMAIL")
#         password = request.args.get("password", "NO_PASSWORD")
#     elif request.method == "POST":
#         email = request.form.get("email", "NO_EMAIL")
#         password = request.form.get("password", "NO_PASSWORD")
#     return render_template("submit.html", email=email, password=password)

@app.route("/upload_file")
def upload_file():
    return render_template("upload_file.html") 

def file_format_is_allowed(file_name):
    file_format = file_name.split('.')[-1]
    file_format = '.' + file_format
    aff = ['.jpeg', '.jpg', '.png', '.gif']  # allowed file formats
    naff = ['', '.html', '.php', '.bat', '.htm', '.xml', '.iso', '.exe', '.js', '.db']  # not allowed file formats
    stat = True

    if file_format not in aff  or file_format in naff:
        stat = False

    return stat

@app.route("/after_upload", methods=["post"])
def after_upload():
    try:
        this_file = request.files["file"]
        if file_format_is_allowed(this_file.filename):
            try:
                dst_path = os.path.join(path, this_file.filename) # uploaded_files/<second arg>
                this_file.save(dst_path)
                res = this_file.filename + '  saved'
            except Exception as e:
                res = "error in saving file \n error: \n " + e
        else:
            res = "The file name is invalid or the format is not allowed \n "

    except  Exception as e:
        res = "ERROR \n " + e
    return res

@app.route("/redirect")
def redirector():
    # return redirect("/login")
    return redirect(url_for("hello"))  # function name in url_for (hello is for "/")

@app.route("/abort")
def aborter():
    abort(404)  # http status_code

@app.errorhandler(404)
def error404handle(error):
    # return "Hi ! \n error is : \n \n \n" + str(error)
    return "Hi ! \n error is : \n \n \n" + str(error), 404  # better than uper one
    # return render_template("error_404.html")
    # return redirect("/")

@app.route("/login_cookie")
def login_cookie():
    # request.cookies for get cookies
    if request.cookies.get("user_email") and session.get("user_password"):  # returns a dictionary
        return "you have already logged in \n welcome your email is: \t \t " + request.cookies["user_email"] + "\t pass:" + session["user_password"]
    else:
        return render_template("form_cookie.html")


@app.route("/submit_cookie", methods=["POST"])
def submit_cookie():
    try:
        email = request.form["email"]  # returns a dictionary
        password = request.form["password"]  # returns a dictionary
        remember = request.form["remember"]


        response = make_response(render_template("submit_cookie.html", email=email, password=password, remember=remember))
        response.set_cookie("user_email", email)  # first one is name of cookie and the second one is its value

        session["user_password"] = password  # session returns a dictionary (sessions doesnt need `make_response`)
        session.permanent = True

        return response
    except Exception as e:
        return f"cookies should be turn ON on your browser \n \n \n {e}"


# db -------------------------------------------------------------------
@app.route("/add_user")
def add_user():
    try:
        user = User(name="test_user")
        db.session.add(user)
        db.session.commit()
        return "add successfully!"
    except Exception as e:
        return "ERROR \t\t" + e


@app.route("/query_db")
def query_db():
    all_users = User.query.all()
    # User.query.filter_by(name="test_user").first()

    str_users = ""
    for i in all_users:
        str_users += str(i)
    
    return str_users







#-----------------------------------------------------------------------