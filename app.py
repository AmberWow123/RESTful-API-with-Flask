from flask import Flask
from flask_restful import Api, Resource, reqparse
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


video_put_args = reqparse.RequestParser()
# it means that the argument passed in is that something
#  we need to be sent through the request
video_put_args.add_argument("name", type=str, help="Name of the video is required", required=True)
video_put_args.add_argument("views", type=int, help="Views of the video is required", required=True)
video_put_args.add_argument("likes", type=int, help="Likes on the video is required", required=True)
# 1st: the name of key
# 2nd: the type of the argument
# 3rd: like an error message if they don't send us this name argument

videos = {}

class Video(Resource):
    def get(self, video_id):
        return videos[video_id]

    # create a video in this put
    def put(self, video_id):
        args = video_put_args.parse_args()
        return {video_id: args}
         

# whenever we send information to this request
# , we need to pass a video id
api.add_resource(Video, "/video/<int:video_id>")

if __name__ == "__main__":
    app.run(debug=True)