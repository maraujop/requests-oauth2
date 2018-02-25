#!/usr/bin/env python3
# Install dependencies with:
# pip install flask requests requests_oauth2
import os
import logging
import requests

from requests_oauth2.services import GoogleClient
from requests_oauth2 import OAuth2BearerToken
from flask import Flask, request, redirect, session


app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(20)


google_auth = GoogleClient(
    client_id=("554229061086-np1qvffgq6gi1f6njg99qkeqt4h2gaut"
               ".apps.googleusercontent.com"),
    client_secret="XqTsoS6DXq-W0KgTqvQISBOM",
    redirect_uri="http://localhost:5000/google/oauth2callback",
)


@app.route("/")
def index():
    return redirect("/google/")


@app.route("/google/")
def google_index():
    if not session.get("access_token"):
        return redirect("/google/oauth2callback")
    with requests.Session() as s:
        s.auth = OAuth2BearerToken(session["access_token"])
        r = s.get("https://www.googleapis.com/plus/v1/people/me")
    r.raise_for_status()
    data = r.json()
    return "Hello, {}!".format(data["displayName"])


@app.route("/google/oauth2callback")
def google_oauth2callback():
    code = request.args.get("code")
    error = request.args.get("error")
    if error:
        return "error :( {!r}".format(error)
    if not code:
        return redirect(google_auth.authorize_url(
            scope=["profile", "email"],
            response_type="code",
        ))
    data = google_auth.get_token(
        code=code,
        grant_type="authorization_code",
    )
    session["access_token"] = data.get("access_token")
    return redirect("/")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    app.run(debug=True)
