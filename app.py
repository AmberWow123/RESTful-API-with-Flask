from flask import Flask
from flask_restful import Api, Resource
# above two models are the main thing we are going to use

app = Flask(__name__)
api = Api(app)

# make a class that is a resource
#  such that it will handle functions like handling a get/put/delete request
class HelloWorld(Resource):
    def get(self):
        return {"data": "Hello World"}

    def post(self):
        return {"data": "Posted"}

# register HelloWorld as a resource
api.add_resource(HelloWorld, "/helloworld")
#  this is gonna be accessible at '/helloworld'

if __name__ == "__main__":
    app.run(debug=True)