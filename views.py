from h3acnvcallsWebService import app

@app.route("/")
def index():
    return "Hello World"