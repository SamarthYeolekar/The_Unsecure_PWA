from flask import Flask, render_template, request, redirect, session
import user_management as dbHandler
from flask_wtf.csrf import CSRFProtect
from flask_talisman import Talisman

app = Flask(__name__)
app.secret_key = 'your_secret_key'
csrf = CSRFProtect(app)
talisman = Talisman(app)

@app.route("/success.html", methods=["POST", "GET", "PUT", "PATCH", "DELETE"])
@csrf.exempt
def addFeedback():
    if request.method == "GET" and request.args.get("url"):
        url = request.args.get("url", "")
        return redirect(url, code=302)
    if request.method == "POST":
        feedback = request.form["feedback"]
        dbHandler.insertFeedback(feedback)
        dbHandler.listFeedback()
        return render_template("/success.html", state=True, value="Back")
    else:
        dbHandler.listFeedback()
        return render_template("/success.html", state=True, value="Back")

@app.route("/signup.html", methods=["POST", "GET", "PUT", "PATCH", "DELETE"])
@csrf.exempt
def signup():
    if request.method == "GET" and request.args.get("url"):
        url = request.args.get("url", "")
        return redirect(url, code=302)
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        DoB = request.form["dob"]
        dbHandler.insertUser(username, password, DoB)
        return render_template("/index.html")
    else:
        return render_template("/signup.html")

@app.route("/index.html", methods=["POST", "GET", "PUT", "PATCH", "DELETE"])
@app.route("/", methods=["POST", "GET"])
@csrf.exempt
def home():
    if request.method == "GET" and request.args.get("url"):
        url = request.args.get("url", "")
        return redirect(url, code=302)
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        isLoggedIn = dbHandler.retrieveUsers(username, password)
        if isLoggedIn:
            dbHandler.listFeedback()
            return render_template("/success.html", value=username, state=isLoggedIn)
        else:
            return render_template("/index.html")
    else:
        return render_template("/index.html")

if __name__ == "__main__":
    app.config.update(
        SESSION_COOKIE_SAMESITE="Lax",
        SESSION_COOKIE_SECURE=True,
        TEMPLATES_AUTO_RELOAD=True,
        SEND_FILE_MAX_AGE_DEFAULT=0,
    )
    app.run(debug=True, host="0.0.0.0", port=5000)