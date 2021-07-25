from flask import Flask
from flask_restful import Api, Resource
# above two models are the main thing we are going to use

app = Flask(__name__)
api = Api(app)

@app.route("/")
def index():
    return "hello, world!"

if __name__ == "__main__":
    app.run(debug=True)