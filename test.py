# this file is to send a request
import requests

# base URL (check when run the flask app)
BASE = "http://127.0.0.1:5000/"

# response = requests.get(BASE + "helloworld/Amber")

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

input() # we can pause for a while til we hit enter

response = requests.get(BASE + "video/2")
# this will send whatever stored inside the videos dict
print(response.json())