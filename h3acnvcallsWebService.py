from flask import Flask
from views import setup_routes
import os
import db
import csv
app = Flask(__name__)

# check if database exists. If it does not exist, create the database
if not os.path.exists("database.db"):
    db.create_database()

setup_routes(app)

if __name__ == "__main__":
    app.run()