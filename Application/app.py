import os
from algorithm import CAT, generate_bank, recognize_speech, setup_questionbank, get_audio_file
from flask import Flask, render_template, request, redirect, session
import speech_recognition as sr
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import pandas as pd
import numpy as np

app = Flask(__name__)

# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
# Session(app)

@app.route("/")
def index():
    # Adaptive Test
    #session['items'] = generate_bank()
    
    session['questionbank'] = pd.read_csv('resource/questionbank.csv')
    diff = session['questionbank']['Difficulty']
    session['items'] = setup_questionbank(diff)

    print(session['items'])
    session['cat'] = CAT(session['items'])

    # Pronounciation
    session['words'] = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

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
        question = str(item_index) + ' ' + str(session['items'][item_index][1])
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
        question = str(item_index) + ' ' + str(session['items'][item_index][1])

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
    
    # Get correct pronounciation audio link from Shtooka
    pronounciation_dict = get_audio_file(word)
    
    return render_template("result_voice.html", result = result, word= word, answer = answer, pronounciation_dict = pronounciation_dict)