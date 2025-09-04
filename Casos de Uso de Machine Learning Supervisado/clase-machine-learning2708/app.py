from flask import Flask, render_template
from casos_data import casos
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", casos=casos)

@app.route("/caso/<id>")
def caso(id):
    c = next((x for x in casos if x["id"] == id), None)
    return render_template("caso.html", caso=c)

if __name__ == "__main__":
    app.run(debug=True)
