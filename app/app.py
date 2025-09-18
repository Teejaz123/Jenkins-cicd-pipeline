from . import app

@app.route("/status")
def status():
    return {"status": "OK"}

