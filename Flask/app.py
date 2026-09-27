from flask import Flask
app=Flask(__name__)

@app.route('/')
def welcome():
    return "Welcome to the Flask application!"
@app.route('/index')
def index():
    return "This is the index page!"


if __name__=="__main__":
    app.run(debug=True)