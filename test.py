import pyrebase
import json
# from distance import distance


config = {
    "apiKey": "AIzaSyCj8R0iJmoT-hlfETLGdTYxzk5VUQ9CLBw",
    "authDomain": "mechatronic-project-af507.firebaseapp.com",
    "databaseURL": "https://mechatronic-project-af507-default-rtdb.firebaseio.com",
    "projectId": "mechatronic-project-af507",
    "storageBucket": "mechatronic-project-af507.appspot.com",
    "messagingSenderId": "782997268535",
    "appId": "1:782997268535:web:0f36553a1637a1400977b2"
    

};


firebase = pyrebase.initialize_app(config)



storage = firebase.storage()
database = firebase.database()

database.child("Test_Data5")
# data = {"key1": a}
data = {"Weight": 1222, "Name": "Thai", "Type": 2, "Orgin":"Lam Dong", "Date_Export": 1712833}
            # database.set(data)
database.set(data)
# data_get = database.child("Test_Data").get().val()


