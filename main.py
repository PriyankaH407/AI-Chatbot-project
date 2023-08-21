//usin Pycharm


from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import pyttsx3
import speech_recognition as sr
import threading
import tkinter as tk

# Initialize text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def speak(text):
    engine.say(text)
    engine.runAndWait()


# Create and train the chatbot
bot = ChatBot("My Bot")
convo = [
    'hello',
    'hi there!',
    'what is your name?',
    'My name is Bot, I am created by Durgesh',
    'how are you?',
    'I am doing great these days',
    'thank you',
    'In which city do you live?',
    'I live in Lucknow',
    'In which language do you talk?',
    'I mostly talk in English'
]
trainer = ListTrainer(bot)
trainer.train(convo)

# Create the GUI
main = tk.Tk()
main.geometry("500x650")
main.title("My Chat bot")

# Load and display the image
img = tk.PhotoImage(file="bot1.png")
photoL = tk.Label(main, image=img)
photoL.pack(pady=5)

# Create chat history frame
frame = tk.Frame(main)
sc = tk.Scrollbar(frame)
msgs = tk.Listbox(frame, width=80, height=20, yscrollcommand=sc.set)
sc.pack(side=tk.RIGHT, fill=tk.Y)
msgs.pack(side=tk.LEFT, fill=tk.BOTH, pady=10)
frame.pack()

# Create text field
textF = tk.Entry(main, font=("Verdana", 20))
textF.pack(fill=tk.X, pady=10)

# Create "Ask from bot" button and functionality
def ask_from_bot():
    query = textF.get()
    answer_from_bot = bot.get_response(query)
    msgs.insert(tk.END, "you : " + query)
    msgs.insert(tk.END, "bot : " + str(answer_from_bot))
    speak(str(answer_from_bot))
    textF.delete(0, tk.END)
    msgs.yview(tk.END)

btn = tk.Button(main, text="Ask from bot", font=("Verdana", 20), command=ask_from_bot)
btn.pack()

# Bind the Enter key to the "Ask from bot" button
def enter_function(event):
    btn.invoke()

main.bind('<Return>', enter_function)

# Function for voice input and conversion to text
def takeQuery():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Your bot is listening. Try to speak.")
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language='en-in')
            print(query)
            textF.delete(0, tk.END)
            textF.insert(0, query)
            ask_from_bot()
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
        except sr.RequestError:
            print("Sorry, I'm currently unavailable.")

# Start a thread to continuously listen for voice input
def repeatL():
    while True:
        takeQuery()

t = threading.Thread(target=repeatL)
t.start()

main.mainloop()
