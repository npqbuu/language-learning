from algorithm import CAT, generate_bank, recognize_speech
from flask import Flask, render_template, request, redirect, session
from flask_session import Session
import speech_recognition as sr
import urllib
from bs4 import BeautifulSoup

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():
    session['items'] = generate_bank()
    session['cat'] = CAT(session['items'])
    session['words'] = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

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
        session['word'] = session['words'].pop()
        word = session['word']
    return render_template("pronounciation.html", word = word, result = result)

@app.route("/checkpronounciation", methods=['POST'])
def checkpronounciation():
    # Open file and write binary (blob) data
    with open('static/pronounciation_user.wav', 'wb') as f:
        f.write(request.data)
    # Speech recognition
    response = recognize_speech(sr.Recognizer(), sr.AudioFile('static/pronounciation_user.wav'))
    session['answer'] = response['transcription']
    
    return redirect('/result_voice')

@app.route("/result_voice")
def result_voice():
    word = session['word']
    answer = session['answer']
    if answer != None:
        result = (word.lower() == answer.lower())
    else:
        result = "Unable to recognize speech"

    # Get correct pronounciation mp3 file from online dictionary Lexico
    url = 'https://www.lexico.com/en/definition/' + word.lower()
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, features='lxml')
    list_audios = soup.find_all('audio')
    for link in list_audios:
        try:
            urllib.request.urlretrieve(link['src'], 'static/pronounciation_dict.wav')
            break
        except:
            print('Broken link')

    return render_template("result_voice.html", result = result, word= word, answer = answer)