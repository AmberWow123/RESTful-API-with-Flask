from flask import Flask
from flask_restful import Api, Resource, reqparse, abort
# above two models are the main thing we are going to use
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return (f"Video(name = {self.name}, views = {self.views}, likes = {self.likes})")


# db.create_all()         # only run once


video_put_args = reqparse.RequestParser()
# it means that the argument passed in is that something
#  we need to be sent through the request
video_put_args.add_argument(
    "name", type=str, help="Name is required", required=True)
video_put_args.add_argument(
    "views", type=int, help="Views is required", required=True)
video_put_args.add_argument(
    "likes", type=int, help="Likes is required", required=True)


videos = {}


class Video(Resource):
    def get(self, video_id):
        return videos[video_id]

    # create a video in this put
    def put(self, video_id):
        # make sure that we don't create a video that already exists
        args = video_put_args.parse_args()
        videos[video_id] = args
        return videos[video_id], 201
        # the status code 201 stands for 'created'

    def delete(self, video_id):
        del videos[video_id]
        return '', 204
        # 204 as deleted successfully


# whenever we send information to this request
# , we need to pass a video id
api.add_resource(Video, "/video/<int:video_id>")

if __name__ == "__main__":
    app.run(debug=True, port=3000)
