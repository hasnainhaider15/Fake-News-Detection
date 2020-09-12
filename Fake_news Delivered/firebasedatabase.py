import pyrebase
import requests
import json

config = {
    "apiKey": "AIzaSyBnkVSKmHpiiVpVU2jtNU9pgyO6eVH2sb8",
    "authDomain": "fakenewsdetection-6ead1.firebaseapp.com",
    "databaseURL": "https://fakenewsdetection-6ead1.firebaseio.com",
    "projectId": "fakenewsdetection-6ead1",
    "storageBucket": "fakenewsdetection-6ead1.appspot.com",
    "messagingSenderId": "873426139624",
    "appId": "1:873426139624:web:97a2a8ce8c845555aacc5d",
    "measurementId": "G-85CRYZJNV6"
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()
auth = firebase.auth()


class DatabaseModel:
    def __init__(self,name,username,password):
        self.name = name
        self.username = username
        self.password = password
        

    def login(self):
        try:
            signin = auth.sign_in_with_email_and_password(self.username, self.password)
            return signin
        except requests.exceptions.HTTPError as e:
            error_json = e.args[1]
            error = json.loads(error_json)['error']
            error = error["message"]
            return error
            
    def register(self):
        data = {"name": self.name, "username": self.username,
                "password": self.password}
        try:
            abc = auth.create_user_with_email_and_password(
                self.username, self.password)
            msg = db.child("users").push(data)
            # msg = msg['name']
            return msg
        except requests.exceptions.HTTPError as e:
            error_json = e.args[1]
            error = json.loads(error_json)['error']
            error = error["message"]
            return error

    def paswordReset(self):
        try:
            send = auth.send_password_reset_email(self.username)
            return send
        except requests.exceptions.HTTPError as e:
            error_json = e.args[1]
            error = json.loads(error_json)['error']
            error = error["message"]
            return error
