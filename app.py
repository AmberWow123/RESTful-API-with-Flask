from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
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


video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str, help="Name of the video")
video_update_args.add_argument("views", type=int, help="Views of the video")
video_update_args.add_argument("likes", type=int, help="Likes of the video")


# we are making this dictionary here
# it will define the fields from the VideoModel above
resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer
}


class Video(Resource):
    # it means that when the class method return
    # take the return value and serialize it using 'resource_fields'
    # so it assumes we have 'id', 'name', 'views' and 'likes' in the instance
    # then, serialize it into json format that can be returned
    @marshal_with(resource_fields)
    def get(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        # to filter all of the videos with the video_id we have
        # then we return the first response (or first entry in that filter)

        if not result:
            abort(404, message="Could not find video with that id...")

        return result

    @marshal_with(resource_fields)
    # create a video in this put
    def put(self, video_id):
        args = video_put_args.parse_args()

        result = VideoModel.query.filter_by(id=video_id).first()
        if result:  # if exists, then video_id already exists
            abort(409, message="Video id has been taken...")

        # access each value in args individually and use them to create a new VideoModel
        video = VideoModel(id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
        db.session.add(video)       # temporarily adding this video to the database
        db.session.commit()         # it's permanently put in the database
        return video, 201

    @marshal_with(resource_fields)
    def patch(self, video_id):
    # update the video info
        # get all the arguments to update the video info
        args = video_update_args.parse_args()

        # check if the video exists or not
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Video doesn't exist, so cannot update it")

        if args['name']:
            result.name = args['name']
        if args['views']:
            result.views = args['views']
        if args['likes']:
            result.likes = args['likes']

        # we can just commit any changes that we made on the object
        db.session.commit()

        return result

    def delete(self, video_id):
        # del videos[video_id]
        return '', 204
        # 204 as deleted successfully


# whenever we send information to this request
# , we need to pass a video id
api.add_resource(Video, "/video/<int:video_id>")

if __name__ == "__main__":
    app.run(debug=True, port=3000)
