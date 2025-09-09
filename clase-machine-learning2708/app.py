from flask import Flask, render_template, request
from casos_data import casos
import regression_model as rl

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html", casos=casos)

@app.route("/casos")
def casos_view():
    return render_template("index.html", casos=casos)

@app.route("/caso/<id>")
def caso(id):
    c = next((x for x in casos if x["id"] == id), None)
    return render_template("caso.html", caso=c, casos=casos)

@app.route("/regresion-lineal/conceptos")
def regresion_conceptos():
    referencias = [
        "Montgomery, D. C., Peck, E. A., & Vining, G. G. (2021). Introduction to Linear Regression Analysis. Wiley.",
        "James, G., Witten, D., Hastie, T., & Tibshirani, R. (2021). An Introduction to Statistical Learning (2nd ed.). Springer.",
        "Wooldridge, J. M. (2016). Introductory Econometrics: A Modern Approach (6th ed.). Cengage."
    ]
    return render_template("regresion_conceptos.html", referencias=referencias, casos=casos)

@app.route("/regresion-lineal/ejercicio", methods=["GET", "POST"])
def regresion_ejercicio():
    # Asegurar que el modelo esté cargado y entrenado
    rl.ensure_model()
    plot_png = rl.get_training_plot()
    prediccion = None
    valores = None

    # Si el usuario envía datos para predecir
    if request.method == "POST":
        try:
            horas_estudio = float(request.form.get("x1"))
            horas_sueno = float(request.form.get("x2"))
            prediccion = rl.predict(horas_estudio, horas_sueno)
            valores = {"x1": horas_estudio, "x2": horas_sueno}
        except (TypeError, ValueError):
            prediccion = "Error: ingresa números válidos."

    # Obtener descripciones y flujo general
    descripcion_dataset = rl.get_dataset_description()
    descripcion_texto = rl.get_dataset_description_text()
    workflow_description = rl.get_workflow_description()

    # Renderizar plantilla con todas las variables necesarias
    return render_template(
        "regresion_ejercicio.html",
        plot_png=plot_png,
        prediccion=prediccion,
        valores=valores,
        descripcion_dataset=descripcion_dataset,
        descripcion_texto=descripcion_texto,
        workflow_description=workflow_description,
        casos=casos
    )

if __name__ == "__main__":
    app.run(debug=True)
