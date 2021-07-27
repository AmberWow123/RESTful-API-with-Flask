# this file is to send a request
import requests

# base URL (check when run the flask app)
BASE = "http://127.0.0.1:3000/"


response = requests.get(BASE + "video/2")
print(response.json())

response = requests.patch(BASE + "video/2", {})
print(response.json())
