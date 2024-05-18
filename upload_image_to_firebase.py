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
# database = firebase.database()
storage.child("Test_Data/test1.jpg").put('durian_test.jpg')
storage.child("Test_Data/test2.jpg").put('sầu riêng.png')
storage.child("Test_Data/test2.jpg").download('','hello.png')
storage.child("Test_Data/test1.jpg").download('','hello1.png')