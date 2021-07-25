# this file is to send a request
import requests

# base URL (check when run the flask app)
BASE = "http://127.0.0.1:5000/"

response = requests.get(BASE + "helloworld")
print(response.json())
