from flask import Flask, render_template

app = Flask(__name__, template_folder='templates')

@app.route("/")

def index():
    return render_template("index.html")

@app.route("/demo")

def demo():
    progress = 30
    theta = 0
    # Question variables
    question = "Question title variable"
    choice1 = True
    choice2 = False
    return render_template("demo.html", question = question, theta = theta, progress = progress, choice1 = choice1, choice2 = choice2)