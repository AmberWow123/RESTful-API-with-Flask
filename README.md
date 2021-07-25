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

app.py
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

## Passing Argument

app.py
```python
...
class HelloWorld(Resource):
    def get(self, name, test):
        return {"name": name, "test": test}
api.add_resource(HelloWorld, "/helloworld/<string:name>/<int:test>")
...
```
> this means that we want user to type something after '/helloworld/'

test.py
```python
...
response = requests.get(BASE + "helloworld/Amber/23")
...
```
> And, we are gonna to pass that in request

Output
```terminal
{'name': 'Amber', 'test': 23}
```

## Storing Data in Memory
