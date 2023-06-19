from app.base import app


@app.route("/ping")
def ping():
    return "pong"


@app.route("/db_ping")
def db_ping():
    return "pong"
