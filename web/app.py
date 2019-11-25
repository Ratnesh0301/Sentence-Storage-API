"""
Registration of a user
Each user gets 10 token
Store a sentence on our database for 1 token
Retrieve his stored sentence on our database for 1 token

"""
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.SentencesDatabase
users = db["Users"]

def verifyPw(username,password):
    hashed_pw = users.find({
        "Username":username,
    })[0]["Password"]

    if bcrypt.hashpw(password.encode("utf8"),hashed_pw)== hashed_pw:
        return True
    else:
        False

def countTokens(username):
    tokens = users.find({
        "Username":username,
    })[0]["Tokens"]
    return tokens

class Register(Resource):

    def post(self):
        #Step1: Get posted data from the user
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]

        hashed_pw = bcrypt.hashpw(password.encode('utf8'),bcrypt.gensalt())

        users.insert({
            "Username":username,
            "Password":hashed_pw,
            "Sentence":"",
            "Tokens":6
        })

        retJson = {
            "status":200,
            "msg":"You successfully signed up for the API"
        }

        return jsonify(retJson)

class Store(Resource):

    def post(self):
        #step1: get the posted data
        postedData = request.get_json()
        #step2: read the posted data
        username = postedData["username"]
        password = postedData["password"]
        sentence = postedData["sentence"]

        #ste3: verify the credentials
        correct_pw = verifyPw(username,password)

        if not correct_pw:
            retJson = {
                "status":302
            }
            return jsonify(retJson)

        
        #step4: verify user has enough tokens
        num_tokens = countTokens(username)

        if num_tokens <= 0:
            retJson = {
                "status":301
            }
            return jsonify(retJson)

        #step5: store the sentence, take one token away and return 200 okay

        users.update({
            "Username":username
        },{
            "$set":{
                "Sentence":sentence,
                "Tokens":num_tokens-1
            }
        })

        retJson = {
            "status":200,
             "msg":"Sentence saved successfully"
        }

        return jsonify(retJson)

class Get(Resource):
    def get(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]

        correct_pw = verifyPw(username,password)

        if not correct_pw:
            retJson = {
                "status":302
            }
            return jsonify(retJson)

        num_tokens = countTokens(username)
        if num_tokens <= 0:
            retJson = {
                "status":301
            }
            return jsonify(retJson)
        
        users.update({
            "Username":username
        },{
            "$set":{
                "Tokens":num_tokens-1
            }
        })

        sentence = users.find({
            "Username":username
        })[0]["Sentence"]

        retJson = {
            "status":200,
            "sentence":sentence
        }

        return jsonify(retJson)

api.add_resource(Register,'/register')
api.add_resource(Store,'/store')
api.add_resource(Get,'/get')

if __name__ == "__main__":
    app.run(host="0.0.0.0")



"""from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")

db = client.aNewDB

UserNum = db['UserNum']

UserNum.insert({
    "num_of_users":0
})

class Visit(Resource):

    def get(self):
        prev_num = UserNum.find({})[0]['num_of_users']
        new_num = prev_num + 1
        UserNum.update({},{"$set":{"num_of_users":new_num}})
        return str("Hello user"+str(new_num))

def checkPostedData(posted_data,function_name):
    if function_name == "add" or "subtract"  or "multiply" :
        if 'x' not in posted_data or 'y' not in posted_data:
            return 301
        else:
            return 200
    elif function_name == "division":
        if 'x' not in posted_data or 'y' not in posted_data:
            return 301
        elif posted_data['y'] == 0:
            return 302
        else:
            return 200


class Add(Resource):
    def post(self):
        posted_data = request.get_json()

        status_code = checkPostedData(posted_data,"add")
        if status_code != 200:
            retJson = {
                "Message":"An ERROR Occured",
                "Status Code" : status_code
            }
        else:
            x = posted_data['x']
            y = posted_data['y']
            x = int(x)
            y = int(y)

            ret = x+y
            retJson = {
                'Message':ret,
                'Status Code':200
            }
        return jsonify(retJson)

class Subtract(Resource):
    def post(self):
        posted_data = request.get_json()

        status_code = checkPostedData(posted_data,"subtract")
        if status_code != 200:
            retJson = {
                "Message":"An ERROR Occured",
                "Status Code" : status_code
            }
        else:
            x = posted_data['x']
            y = posted_data['y']
            x = int(x)
            y = int(y)

            ret = x-y
            retJson = {
                'Message':ret,
                'Status Code':200
            }
        return jsonify(retJson)

class Multiply(Resource):
    def post(self):
        posted_data = request.get_json()

        status_code = checkPostedData(posted_data,"multiply")
        if status_code != 200:
            retJson = {
                "Message":"An ERROR Occured",
                "Status Code" : status_code
            }
        else:
            x = posted_data['x']
            y = posted_data['y']
            x = int(x)
            y = int(y)

            ret = x*y
            retJson = {
                'Message':ret,
                'Status Code':200
            }
        return jsonify(retJson)

class Division(Resource):
    def post(self):
        posted_data = request.get_json()

        status_code = checkPostedData(posted_data,"division")
        if status_code != 200:
            retJson = {
                "Message":"An ERROR Occured",
                "Status Code" : status_code
            }
        else:
            x = posted_data['x']
            y = posted_data['y']
            x = int(x)
            y = int(y)

            ret = x/y
            retJson = {
                'Message':ret,
                'Status Code':200
            }
        return jsonify(retJson)


api.add_resource(Add,"/add")
api.add_resource(Subtract,"/subtract")
api.add_resource(Multiply,"/multiply")
api.add_resource(Division,"/division")
api.add_resource(Visit,"/hello")


@app.route('/')
def helloWorld():
    return "Hello World!"


if __name__ == "__main__":
    app.run(debug=True)"""