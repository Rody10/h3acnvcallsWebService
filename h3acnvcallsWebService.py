from flask import Flask
import os
import db
app = Flask(__name__)

# check if database exists. If it does not exist, create the database
if not os.path.exists("database.db"):
    db.create_database()


@app.route("/")
def hello_world():
    return "Hello World!"

if __name__ == "__main__":
    app.run()