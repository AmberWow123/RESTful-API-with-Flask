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

## Request Argument Parser

