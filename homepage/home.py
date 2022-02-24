from flask import Flask, render_template, redirect, request, url_for, session
import os
import re
import random

app = Flask(__name__)


@app.route("/main")
def main():
    modeString = open("secret/modeString.txt").read()
    htmlcon = ""
    userlist = os.listdir(f"data/{modeString}")

    print(userlist)

    for i in userlist:

        numbers = re.sub(r"[^0-9]", "", i)
        numbers = numbers[0:5] + "*****" + numbers[-6:-1]
        htmlcon += f"<a>user{numbers}</a>"
    return htmlcon


@app.route("/userinfo")
def userinfo(num=None):
    modeString = open("secret/modeString.txt").read()
    if num == None:
        userlist = os.listdir(f"data/{modeString}")
        result = random.choice(userlist)

        numbers = re.sub(r"[^0-9]", "", result)
        randominfo = f"data/{modeString}/{result}/userinfo{numbers}.data"

        with open(randominfo) as f:
            content = f.read()
            content = content.replace("\n", "<br>")
            return content


app.run(debug=True)
