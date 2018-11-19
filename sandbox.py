from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "hello from ghetto"

@app.route('/')
@app.route('/<name>')
def index(name="bob"):
    return "hello {}".format(name)

@app.route('/add/<int:num1>/<int:num2>')
@app.route('/add/<float:num1>/<float:num2>')
@app.route('/add/<float:num1>/<int:num2>')
@app.route('/add/<int:num1>/<float:num2>')
def add(num1,num2):
    return num1 + num2
    return "{} + {} = {}".format(num1,num2,num1+num2)

app.run(debug=True, port=8000, host='0.0.0.0')