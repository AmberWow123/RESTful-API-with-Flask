# this file is to send a request
import requests

# base URL (check when run the flask app)
BASE = "http://127.0.0.1:5000/"

# response = requests.get(BASE + "helloworld/Amber")

response = requests.put(BASE + "video/1", {"likes": 10, "name": "Amber", "views": 1000000})
print(response.json())

input() # we can pause for a while til we hit enter

response = requests.get(BASE + "video/1")
# this will send whatever stored inside the videos dict
print(response.json())