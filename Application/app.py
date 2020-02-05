from flask import Flask, render_template, request
from algorithm import CAT, generate_bank


items = generate_bank()
cat = CAT(items)

app = Flask(__name__, template_folder='templates')

@app.route("/")

def index():
    return render_template("index.html")

@app.route("/demo", methods=["GET", "POST"])

def demo():
    choice1 = True
    choice2 = False

    if request.method == "GET":
        # cat = CAT(items) # Start CAT procedure

        (_stop, item_index) = cat.item_selection() # Get first item
        cat.administered_items.append(item_index)

        progress = 0
        theta = cat.thetas[0]
        # Question variables
        question = str(item_index)
    else:
        answer = request.form.get("answer") # Get user respone for current question
        if answer == "option1":
            response = True
        else:
            response = False
        print(response)

        cat.responses.append(response)
        cat.item_administration()

        (_stop, item_index) = cat.item_selection() # Get next item
        #if _stop:
        #    break
        cat.administered_items.append(item_index)
        progress = (len(cat.thetas) - 1) * 10
        theta = cat.thetas[-1]
        # Question variables
        question = str(item_index)

    # Render Template
    return render_template("demo.html", question = question, theta = theta, progress = progress, choice1 = choice1, choice2 = choice2)