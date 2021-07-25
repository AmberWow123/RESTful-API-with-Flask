from flask import Flask
from flask_restful import Api, Resource
# above two models are the main thing we are going to use

app = Flask(__name__)
api = Api(app)

# # whenever they send us a name,
# # we will send its corresponding value back
# names = {"Amber": {"age": 23, "gender": "female"}, 
#         "Jack": {"age": 26, "gender": "male"}}

# # make a class that is a resource
# #  such that it will handle functions like handling a get/put/delete request
# class HelloWorld(Resource):
#     def get(self, name):
#         return names[name]        

# # register HelloWorld as a resource
# api.add_resource(HelloWorld, "/helloworld/<string:name>")
# #  this is gonna be accessible at '/helloworld'


videos = {}

class Video(Resource):
    def get(self, video_id):
        return videos[video_id]

    # create a video in this put
    def put(self, video_id):
         

# whenever we send information to this request
# , we need to pass a video id
api.add_resource(Video, "/video/<int:video_id>")

if __name__ == "__main__":
    app.run(debug=True)