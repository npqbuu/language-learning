import speech_recognition as sr
from algorithm import recognize_speech

response = recognize_speech(sr.Recognizer(), sr.AudioFile('file.wav'))
print(response)