import speech_recognition as sr
from algorithm import recognize_speech_from_mic

# create recognizer and mic instances
recognizer = sr.Recognizer()
microphone = sr.Microphone()

text = recognize_speech_from_mic(recognizer, microphone)
print(text['transcription'])

# TODO: Convert to client side recording (https://www.reddit.com/r/flask/comments/6wg24z/is_there_any_tutorial_on_how_to_run_pyaudio_with/) -> Learn JavaScript