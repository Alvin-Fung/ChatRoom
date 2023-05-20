from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import SocketIO, send, join_room, leave_room
import random
from string import ascii_uppercase

app = Flask(__name__)
app.config["SECRET_KEY"] = "thefungchat"
socketio = SocketIO(app)

rooms = {}

def generate_unique_code(Length):
    while True:
        code = ""
        for _ in range(Length):
            code += random.choice(ascii_uppercase)
        
        if code not in rooms:
            break
        
    return code

@app.route("/", methods = ["POST","GET"])
def login():
    session.clear()
    if request.method == "POST":
        name = request.form.get("name")
        code = request.form.get("code")
        #.get will attempt to the dictionary(form)
        #safer method of acquiring a value associated within the form
        #both join and create will have empty values
        join = request.form.get("join", False) 
        create = request.form.get("create", False)
        
        if not name:
            return render_template("login.html", error="Please enter a name!", code=code, name=name)
        
        if join != False and not code:
            return render_template("login.html", error="Please enter a room code!", code=code, name=name)
        
        #Room creation
        room = code
        if create != False: #"if they're not creating a room, then they must be joining a room."
            room = generate_unique_code(4)
            rooms[room] = {"members": 0, "messages": []} #Starting data for room dictionary
        elif code not in rooms: 
            return render_template("login.html", error="Room does not exist.")
        
        session["room"] = room #Storing info about a user, instead of using logins for now.
        session["name"] = name
        return redirect(url_for("room")) #Redirecting the user to the chat 
        
    return render_template("login.html")

@app.route("/room")
def room():
    #Guard clause
    room = session.get("room")
    if room is None or session.get("name") is None or room not in rooms:
        return redirect(url_for("login"))
    
    return render_template("room.html")

#Initializer
if __name__ == "__main__":
    socketio.run(app, debug=True)
