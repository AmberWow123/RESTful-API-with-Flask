# RESTful-API-with-Flask

## Setup
```
pip install -r requirements.txt
```

## Run
```
python app.py
```
## Run Test
the ```test.py``` file send a **request**
(first run ```app.py``` then run ```test.py```)
```
python test.py
```

--- 
## Handling post/get request

### ```test.py```
```python
import requests

# base URL 
# (check the terminal output when run the flask app)
BASE = "http://127.0.0.1:5000/"

response = requests.post(BASE + "helloworld")
# response = requests.get(BASE + "helloworld")
print(response.json())
```
> ```get``` and ```post``` are the methods we wrote in ```app.py```

### ```app.py```
```python
...
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
...
```

### Output

> if we have response = requests.post(BASE + "helloworld") in ```test.py```
```terminal
{"data": "Posted"}
```
> otherwise, if we have response = requests.get(BASE + "helloworld") in ```test.py```
```terminal
{"data": "Hello World"}
```
---
## Passing Argument

### ```app.py```
```python
...
class HelloWorld(Resource):
    def get(self, name, test):
        return {"name": name, "test": test}
api.add_resource(HelloWorld, "/helloworld/<string:name>/<int:test>")
...
```
> this means that we want user to type something after '/helloworld/'

### ```test.py```
```python
...
response = requests.get(BASE + "helloworld/Amber/23")
...
```
> And, we are gonna to pass that in request

### Output
```terminal
{'name': 'Amber', 'test': 23}
```
---
## Storing Data in Memory

### ```app.py```

> Store a dictionary ```names``` with the corresponding values of specific name
```python
...
# whenever they send us a name,
# we will send its corresponding value back
names = {"Amber": {"age": 23, "gender": "female"}, 
        "Jack": {"age": 26, "gender": "male"}}

class HelloWorld(Resource):
    def get(self, name):
        return names[name]

api.add_resource(HelloWorld, "/helloworld/<string:name>")
...
```

### ```test.py```
```python
...
response = requests.get(BASE + "helloworld/Amber")
...
```

> When it sends a request with a given name, it will response back with the corresponding values of the given name
---
## Get Data from a Request

### ```test.py```
```python
...
response = requests.put(BASE + "video/1", {"like": 10})
...
```

### ```app.py```
```python
...
class Video(Resource):
    def get(self, video_id):
        return videos[video_id]

    # create a video in this put
    def put(self, video_id):
        print(request.method) 
            # this will print out 'put'
            # since we are inside the put method
        print(request.form)
            # this will print out the data we sent through the request
            # which is the 2nd parameter inside requests.put(BASE + "video/1", {"like": 10})
        print(request.form["like"])
            # it will print out a int value of 10
        ...
...
```
---
## Request Argument Parser

> There is a better way to use request
* The built-in method of Flask Restful called request parser

### Import reqparse in ```app.py```
```python
from flask_restful import reqparse
```
### Make a New Request Parser Object in ```app.py```
> we are gonna to make a new request parser object 
```python
...
video_put_args = reqparse.RequestParser()
...
```
> this request parser object will automatically parse through the sent request 

> to ensure that the sent request kinda fits the defined guidelines and has the correct information in it

> if it is correct, then it will allow us to grab all the information very easily by using a method called parse args

### ```app.py```
```python
from flask import Flask
from flask_restful import Api, Resource, reqparse
app = Flask(__name__)
api = Api(app)
video_put_args = reqparse.RequestParser()
# it means that the argument passed in is that something
#  we need to be sent through the request
video_put_args.add_argument("name", type=str, help="Name of the video is required")
video_put_args.add_argument("views", type=int, help="Views of the video is required")
video_put_args.add_argument("likes", type=int, help="Likes on the video is required")
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
         
api.add_resource(Video, "/video/<int:video_id>")

if __name__ == "__main__":
    app.run(debug=True)
```
### ```test.p```
```python
...
response = requests.put(BASE + "video/1", {"likes": 10})
...
```

### Output
> the values of keys 'name' and 'views' are both ```None```

> it's because we didn't send anything with them
```terminal
{'1': {'name': None, 'views': None, 'likes': 10}}
```

### Error Message When the Request Doesn't Fit

### ```app.py```
```python
...
video_put_args.add_argument("name", type=str, help="Name of the video is required", required=True)
video_put_args.add_argument("views", type=int, help="Views of the video is required", required=True)
video_put_args.add_argument("likes", type=int, help="Likes on the video is required", required=True)
...
```
### Output
> It's telling us that the argument you sent is invalid

> the argument 'name' is the thing we are looking for, but it is not passed in, then the error message appears
```terminal
{'message': {'name': 'Name of the video is required'}}
```
---

## Sending Status Code

### ```app.py```
```python
...
class Video(Resource):
    def get(self, video_id):
        return videos[video_id]

    # create a video in this put
    def put(self, video_id):
        args = video_put_args.parse_args()
        videos[video_id] = args
        return videos[video_id], 201
        # the status code 201 stands for 'created'
        # 200 stands for 'Okay' (Nothing goes wrong)
...
```

### ```test.py```
```python
...
response = requests.put(BASE + "video/1", {"likes": 10, "name": "Amber", "views": 1000000})
print(response.json())

input() # we can pause for a while til we hit enter

response = requests.get(BASE + "video/1")
# this will send whatever stored inside the videos dict
print(response.json())
```

### Output
```terminal
{'name': 'Amber', 'views': 1000000, 'likes': 10}
<Enter>
{'name': 'Amber', 'views': 1000000, 'likes': 10}
```
---
## Validating Requests
To make sure that we don't actually crash if we ask for some key (ex. video_id) that doesn't exist

### Import ```abort``` in ```app.py```
```python
from flask_restful import abort
```

### Write an validating function in ```app.py```
```python
# check if the video_id passed in actually exists or not
def abort_if_video_id_not_exist(video_id):
    if video_id not in videos:
        abort(404, message="Could not find such a video id...")
        # 404 as 'could not found'

class Video(Resource):
    def get(self, video_id):
        abort_if_video_id_not_exist(video_id)               # added
        return videos[video_id]
...
```
### ```test.py```
```python
response = requests.get(BASE + "video/5")       # passed in an non-exist video_id
print(response.json())
```

### Output
> Since there is no such video id, ```abort()``` is called and the error message is printed
```terminal
{'message': 'Could not find such a video id...'}
```

---
## Handling Delete Requests
We now completed ```put()``` and ```delete()``` by checking whether or not the video id exist

### ```app.py```
```python
...
def abort_if_video_id_not_exist(video_id):
    if video_id not in videos:
        abort(404, message="Could not find such a video id...")
        # 404 as 'could not found'

def abort_if_video_exists(video_id):
    if video_id in videos:
        abort(409, message="Video already exists with that ID...")

class Video(Resource):
    # get video info with a given video id
    def get(self, video_id):
        abort_if_video_id_not_exist(video_id)
        return videos[video_id]

    # create a video
    def put(self, video_id):
        # make sure that we don't create a video that already exists
        abort_if_video_exists(video_id)
        args = video_put_args.parse_args()
        videos[video_id] = args
        return videos[video_id], 201    # 201 as 'created'
    
    # delete a video
    def delete(self, video_id):
        # make sure that we don't delete a video that doesn't exist
        abort_if_video_id_not_exist(video_id)
        del videos[video_id]
        return '', 204                  # 204 as 'deleted successfully'
...
```
### ```test.py```
> Create 3 videos with video id from 0 to 2
```python
data = [
    {"likes": 9999999999999, "name": "Girls' Generation - Gee", "views": 10000000000000},
    {"likes": 1000, "name": "How to make RESTful API", "views": 3000},
    {"likes": 10, "name": "Amber", "views": 70000}
]

for i in range(len(data)):
    response = requests.put(BASE + "video/" + str(i), data[i])
    print(response.json())

input()
response = requests.delete(BASE + "video/0")
print(response)         
# for requesting a delete method, it returns a blank string such that there is no .json format at all

input()
response = requests.get(BASE + "video/2")
print(response.json())
```
> Then, delete the video 0 and get the video info of video 2
### Output
```terminal
{'name': "Girls' Generation - Gee", 'views': 10000000000000, 'likes': 9999999999999}
{'name': 'How to make RESTful API', 'views': 3000, 'likes': 1000}
{'name': 'Amber', 'views': 70000, 'likes': 10}
<Enter>
<Response [204]>
<Enter>
{'name': 'Amber', 'views': 70000, 'likes': 10}
```

---
## Database Configuration
Rather than using memory as what we have done so far, we can get all these to be stored in a persistent database

### Install Database
> Okay to skip this part if you have '```pip install -r requirements.txt```'

```python
pip install Flask-SQLAlchemy
```

### Import SQL Alchemy in ```app.py```
```python
from flask_sqlalchemy import SQLAlchemy
```

### Connect to Database in ```app.py```
```python
app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)        
        # 100 as the amount of potential chars
        # nullable=False means there should some text standing for the name of the video
    views = db.Column(db.Integer, nullable=False) 
    likes = db.Column(db.Integer, nullable=False) 

    def __repr__(self):
        return (f"Video(name = {self.name}, views = {self.views}, likes = {self.likes})")

db.create_all()         # only run once
# comment out this line after the first run
# otherwise, the database will be overwrited everytime you run
```

### Error: Instance of 'SQLAlchemy' has no 'Column' member
1. Open the Command Palette (Command+Shift+P on macOS and Ctrl+Shift+P on Windows/Linux) and type in ```Python: Select Linter```

2. Switch from PyLint to flake8 or other supported linters

> Then, there might be some formatting error, but easy to solve

---
## 

---
##