from flask import Flask, render_template, request, session, redirect
from flask_socketio import SocketIO, send, join_room, leave_room
import random
from string import ascii_uppercase

app = Flask(__name__)
app.config["SECRET_KEY"] = "thefungchat"
socketio = SocketIO(app)

#First root - Homepage
@app.root("/frontend/", methods = ["POST","GET"])
def home():
    return render_template("login.html")

#Second root - Chat room



#Initializer
if __name__ == "__main__":
    socketio.run(app, debug=True)
