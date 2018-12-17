from flask import Flask, url_for, render_template, request, make_response
import requests
from sklearn.externals import joblib
app = Flask(__name__)

darksky_key = "09b8629b237840eda0035994d28f0790"
ipstack_key = "666b67a5116ec4d53e1e314954dbb92d"

darksky = requests.get("https://api.darksky.net/forecast/09b8629b237840eda0035994d28f0790/37.8267,-122.4233")
ipstack = requests.get("http://api.ipstack.com/84.14.157.66?access_key=666b67a5116ec4d53e1e314954dbb92d")

@app.route('/', methods=["GET", "POST"])

def index():
    if request.method == "GET":
        return render_template("index.html", name="Thao")

    elif request.method == "POST":
        nom = request.form["nom_utilisateur"]
        prenom = request.form["prenom_utilisateur"]
        email = request.form["email"]
        response = make_response(render_template("project.html"))
        return response

@app.route("/project", methods=["GET", "POST"])
def project():

    current_location = requests.get("http://api.ipstack.com/84.14.157.66?access_key={}".format(ipstack_key))
    current_location = current_location.json()
    ville = current_location["city"]

    weather = requests.get("https://api.darksky.net/forecast/{}/48.866667,2.333333".format(darksky_key))
    weather = weather.json()

    if request.method == "GET":
        return render_template("project.html", weather = weather, ville = ville)
    elif request.method == "POST":
        nom = request.form["nom_utilisateur"]
        prenom = request.form["prenom_utilisateur"]
        email = request.form["email"]
        password = request.form["password"]
        response = make_response(render_template("project.html", weather = weather, ville= ville,
        name = nom,
        email = email,))

@app.route("/urls")
def urls():
    return url_for("about")

@app.route("/predict", methods=["GET", "POST"])
def predict():
    regression = joblib.load("./linear_regression_model.pkl")
    xp = [[float(request.form["regression"])]]
    y_pred = float(regression.predict(xp))
    return render_template('predict.html', xp = xp[0][0] , y_pred = y_pred)

if __name__=="__main__":
    app.run(debug=True)

#1 créer l'algo
#1 enregistrer l'algo
#1 algo.pkl
#1 pluguer dans notre application
