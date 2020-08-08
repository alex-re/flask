from flask import Flask, render_template, request


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
    return render_template("index-flask.html", neme = "ali") # it looks in templates directory by it self

@app.route("/http_get_method")
def get_method():
    data = request.args['id'] # note: this request is "flask.request"!
    return data