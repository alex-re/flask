from flask import Flask, render_template, request
import os


# make directory named "uploaded_files"
path = os.path.join("uploaded_files")
os.makedirs(path, exist_ok="True")

app = Flask(__name__)


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

@app.route("/after_upload", methods=["post"])
def after_upload():
        this_file = request.files["file"]
        naff = ['', '.html', '.php', '.bat', '.htm', '.xml', '.exe', '.js', '.db'] # not_allowed_file_formats
        if this_file.filename != naff[0] and this_file.filename[-5:] != naff[1] and this_file.filename[-4:] != naff[2] and this_file.filename[-4:] != naff[3] and this_file.filename[-4:] != naff[4] and this_file.filename[-4:] != naff[5] and this_file.filename[-4:] != naff[6] and this_file.filename[-3:] != naff[7] and this_file.filename[-3:] != naff[8] :
            try:
                dst_path = os.path.join(path, this_file.filename) # uploaded_files/<second arg>
                this_file.save(dst_path)
                res = this_file.filename + '  saved'
            except Exception as e:
                res = "error in saving file \n error: \n " + e
        else:
            res = "The file name is invalid \n you cant send blow file types \n "
            for i in naff:
                res = res + '\t' + i
        return res