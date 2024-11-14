from flask import Flask, render_template, request,redirect
import requests
import numpy as np
import pickle
import datetime
import time

app = Flask(__name__)
model = pickle.load(open("static/model_clf.sav", "rb"))

global labels, values
labels = []
values = []

@app.route("/", methods=["POST", "GET"])
def homepage():
    test = False
    done = False
    pred = ""
    if request.method == "POST":
        done = True
        age = request.form.get("age")
        sex = request.form.get("gender")
        cp = request.form.get("cp")
        chol = request.form.get("chol")
        exang = request.form.get("eng")
        trestbps = request.form.get("bp")
        fbs = request.form.get("fbs")
        thalach = request.form.get("hr")
        restecg = get_ecg_value()

        if sex.lower() == "male":
            sex = 1
        else:
            sex = 0

        if cp == "Asymptomatic":
            cp = 0
        elif cp == "Atypical Angina":
            cp = 1
        elif cp == "Non-Anginal Pain":
            cp = 2
        else:
            cp = 3

        if exang.lower() == "yes":
            exang = 1
        else:
            exang = 0
        print("cp:", cp)
        if chol.lower() == "low":
            chol = 1
        else:
            chol = 0
        print("cp:", cp)

        if restecg == None:
            return "please Connect the heartician Device to internet"

        final = [np.array(
            [int(age), int(sex), int(cp), int(chol), int(restecg), int(exang), int(trestbps), int(fbs), int(thalach)])]
        prediction = model.predict_proba(final)
        pred = model.predict(final)
        print(pred)
        output = '{0:.{1}f}'.format(prediction[0][1], 2)
        output = float(output)
        output = output * 100
        output = round(output, 2)
        if pred == 0:
            tes = False
            pred = "The probability of you NOT HAVING a Heart attack is " + str(output) + "% and you are safe."
        else:
            test = True
            pred = "The probability of you HAVING a Heart attack is " + str(output) + "%"
        print(pred)

    return render_template('homepage.html', done=done, pred=pred, test=test)


@app.route("/chart")
def chart():
    global labels, values
    build_data()
    return render_template("chart.html", labels=labels[-5:], values=values[-5:])
@app.route("/cleardata")
def clear():
    global labels, values
    with open("static/labels.txt", "w") as f:
        f.write("")
    with open("static/values.txt", "w") as f:
        f.write("")
    return redirect("/chart")


def build_data():
    global labels, values
    with open("static/labels.txt","r") as f:
        data = f.read()
        labels = data.split(",")
        labels.remove('')
    with open("static/values.txt", "r") as f:
        data = f.read()
        values = data.split(",")
        values.remove("")



# "age","sex","cp", "chol", "restecg","exang","trestbps","fbs","thalach"
"""
Value 0: asymptomatic
Value 1: atypical angina
Value 2: non-anginal pain
Value 3: typical angina
# 'F' - 0, 'M' - 1
# 'High' - 0, 'Low' - 1 (for chol)
# 'LVH' - 0, 'Normal' - 1, 'ST' - 2
"""


def get_ecg_value():
    # Endpoint to retrieve the ECG value
    url = "https://heartican.pythonanywhere.com/getval"

    try:
        # Send GET request to the API
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            ecg_value = data.get("ecgVal")
            if int(ecg_value) < 600:
                ecg_value = 0
            elif 600 < int(ecg_value) < 900:
                ecg_value = 1
            else:
                ecg_value = 2
            return ecg_value
        else:
            print(f"Failed to retrieve ECG value. Status code: {response.status_code}")
            return None
    except:
        return None


if __name__ == '__main__':
    app.run(debug=True)
