#############TEST#############

import sqlite3
from flask import Flask, render_template, request, session, redirect
from flask_socketio import SocketIO
from flask_session import Session



__author__ = "Brian Perret"

#Initialization and configuration of app

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['DEBUG'] = True
app.config["SESSION_PERMANENT"] = False

#start session
Session(app)

#start socketio
socketio = SocketIO(app, async_mode=None, logger=True, engineio_logger=True)


#debbug
print("start")

#home page 
@app.route('/')
def index():
    return render_template('index.html')

"""
@socketio.on('test_message')
def handle_message(data):
    print('received message: ' + str(data))
    socketio.emit('test_socket',{'number': 'Youpie !'})
"""

#received messages :
@socketio.on('message_send')
def message_recu(data):
    print('received message: ' + str(data))
    message_to_send(data)

    


#send messages

def message_to_send(data):

    #user not login  -> anonymous
    if not session.get("username"):

        socketio.emit('message_to_send', {"user" : "anonymous", 'msg' : data})
    else:
        socketio.emit('message_to_send', {"user" : session.get("username"), 'msg' : data})


#login page
@app.route('/login', methods=['GET', 'POST'])
def login():

    #user haven't session 
    if not session.get("username"):
        
        print("l'utilisateur n'a pas de session")

        #user login request 
        if(request.method=='POST'):
             #received login data
            print("l'utilisateur envoie les données d'authentification")

            username = request.form['username']

            #stock data into user's session

            session['username'] = username

            print("user name : ", session.get("username"))

            #redirection user to home page

            return redirect("/")

        else:
            print("l'utilisateur veux se connecté")
            return render_template('sign_in_page.html')

    else:
        #user have session

        print("l'utilisateur se déconnecte")
        return redirect("/sign-out")

@app.route("/sign-up",  methods=['GET', 'POST'])
def sign_up ():

    if request.method == 'POST':
        
        #received login data
        print("l'utilisateur envoie les données d'inscription")

        username = request.form['username']

        #check username already existe:

        bdd = sqlite3.connect('database.db')
        curseur = bdd.cursor()
        req = ('SELECT name FROM playerDB')
        curseur.execute(req)
        data = curseur.fetchall()        

        if not username in data:
            curseur.execute('INSERT INTO playerDB (username,maxScore) VALUES (?,?)', (username, 0))
            print("register username -> sql")
        else:
            #username already exist
            #send message to user
            print("error : user already exist")
            socketio.emit('error', {'msg' : "username already exist"})

        return redirect('/login')
    else:
        
        return render_template('sign_up_page.html')
    




        
        











        """
        try:
            username = request.form['username']
 
            
            with sqlite3.connect("database.db") as db:

                req = db.cursor()

                req.execute("SELECTE username FROM tab")

                data = req.fetchall

                if not username in data:

                    req = db.cursor()
                    req.execute("INSERT INTO tab (username) VALUES (?)", (username))
                    
                    req.commit()
                    msg = "Record successfully added"

                    return redirect("/login")

                else:
                    msg = "username already exist"
        except:
            db.rollback()
            msg = "error in insert operation"
        
        finally:
            db.close()
    
    return render_template("sign_up_page.html")
    """


@app.route("/sign-out")
def logout():
    session["username"] = None
    return redirect("/")

if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=1664)