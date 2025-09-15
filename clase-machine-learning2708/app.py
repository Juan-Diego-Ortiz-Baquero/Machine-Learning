from flask import Flask, render_template, request
from casos_data import casos
import regression_model as rl

app = Flask(__name__)

# ---------------------------
# HOME
# ---------------------------
@app.route("/")
def home():
    return render_template("home.html", casos=casos, active_page='home')

# ---------------------------
# CASOS
# ---------------------------
@app.route("/casos")
def casos_view():
    return render_template("index.html", casos=casos, active_page='casos')

@app.route("/caso/<id>")
def caso(id):
    c = next((x for x in casos if x["id"] == id), None)
    return render_template("caso.html", caso=c, casos=casos, active_page='casos')

# ---------------------------
# REGRESIÓN LINEAL
# ---------------------------
@app.route("/regresion-lineal/conceptos")
def regresion_conceptos():
    referencias = [
        "Statistics Easily. (s. f.). Supuestos en regresión lineal. Recuperado el 9 de septiembre de 2025, de https://es.statisticseasily.com/supuestos-en-regresión-lineal",
        "Universidad de los Andes. (s. f.). Regresión lineal. Recuperado el 9 de septiembre de 2025, de https://programas.uniandes.edu.co/blog/regresion-lineal",
        "Probabilidad y Estadística. (s. f.). Regresión lineal. Recuperado el 9 de septiembre de 2025, de https://www.probabilidadyestadistica.net/regresion-lineal"
    ]
    return render_template("regresion_conceptos.html", referencias=referencias, casos=casos, active_page='regresion_conceptos')

@app.route("/regresion-lineal/ejercicio", methods=["GET", "POST"])
def regresion_ejercicio():
    # Asegurar que el modelo esté cargado y entrenado
    rl.ensure_model()
    plot_png = rl.get_training_plot()
    prediccion = None
    valores = None

    if request.method == "POST":
        try:
            horas_estudio = float(request.form.get("x1"))
            horas_sueno = float(request.form.get("x2"))
            prediccion = rl.predict(horas_estudio, horas_sueno)
            valores = {"x1": horas_estudio, "x2": horas_sueno}
        except (TypeError, ValueError):
            prediccion = "Error: ingresa números válidos."

    descripcion_dataset = rl.get_dataset_description()
    descripcion_texto = rl.get_dataset_description_text()
    workflow_description = rl.get_workflow_description()

    return render_template(
        "regresion_ejercicio.html",
        plot_png=plot_png,
        prediccion=prediccion,
        valores=valores,
        descripcion_dataset=descripcion_dataset,
        descripcion_texto=descripcion_texto,
        workflow_description=workflow_description,
        casos=casos,
        active_page='regresion_ejercicio'
    )

# ---------------------------
# REGRESIÓN LOGÍSTICA
# ---------------------------
@app.route("/regresion-logistica/conceptos")
def r_logistica_conceptos():
    referencias = [
        "Probabilidad y Estadística. (s. f.). Regresión logística. Recuperado el 14 de septiembre de 2025, de https://www.probabilidadyestadistica.net/regresion-logistica/",
        "DataScientest. (s. f.). ¿Qué es la regresión logística? Recuperado el 14 de septiembre de 2025, de https://datascientest.com/es/que-es-la-regresion-logistica",
        "Conceptos Claros. (s. f.). Qué es y cómo interpretar una regresión logística. Recuperado el 14 de septiembre de 2025, de https://conceptosclaros.com/que-es-regresion-logistica/"
    ]
    return render_template("r_logistica_concepto.html", referencias=referencias, casos=casos, active_page='r_logistica_conceptos')

@app.route("/regresion-logistica/ejercicio")
def r_logistica_ejercicio():
    # Por ahora solo muestra un placeholder o plantilla vacía
    return render_template("r_logistica_ejercicio.html", casos=casos, active_page='r_logistica_ejercicio')

# ---------------------------
# MAIN
# ---------------------------
if __name__ == "__main__":
    app.run(debug=True)
