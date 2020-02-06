from algorithm import CAT, generate_bank
from flask import Flask, render_template, request, redirect, session
from flask_session import Session

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():
    session['items'] = generate_bank()
    session['cat'] = CAT(session['items'])

    return render_template("index.html")

@app.route("/demo", methods=["GET", "POST"])
def demo():
    choice1 = True
    choice2 = False

    if request.method == "GET":

        (_stop, item_index) = session['cat'].item_selection() # Get first item
        session['cat'].administered_items.append(item_index)

        progress = 0
        theta = session['cat'].thetas[0]
        # Question variables
        question = str(item_index)
    else:
        answer = request.form.get("answer") # Get user respone for current question
        if answer == "option1":
            response = True
        else:
            response = False
        print(response)

        session['cat'].responses.append(response)
        session['cat'].item_administration()

        (_stop, item_index) = session['cat'].item_selection() # Get next item
        if _stop:
            return redirect('/result')
        session['cat'].administered_items.append(item_index)
        progress = (len(session['cat'].thetas) - 1) * 10
        theta = session['cat'].thetas[-1]
        # Question variables
        question = str(item_index)

    # Render Template
    return render_template("demo.html", question = question, theta = theta, progress = progress, choice1 = choice1, choice2 = choice2)

@app.route("/result")
def result():
    theta = session['cat'].thetas[-1]
    return render_template("result.html", theta = theta)

@app.route("/pronounciation", methods=['GET', 'POST'])
def pronounciation():
    if request.method == "GET":
        result = ''
        word = 'April'
    else:
        #f = request.files['file']
        #filePath = "./somedir/"+secure_filename(f.filename)
        #f.save(filePath)
        app.logger.debug(request.files['file'].filename) 
        result = True

    return render_template("pronounciation.html", word = word, result = result)
