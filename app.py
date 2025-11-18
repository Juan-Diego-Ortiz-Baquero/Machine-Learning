from flask import Flask, render_template, request, current_app, jsonify
from casos_data import casos
import regression_model as rl
import regression_logistica as rlog
import xgb_credit as xgb
import reinforcement_learning as rl_module
import base64
import os

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
    return render_template("casos.html", casos=casos, active_page='casos')

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
        "Conceptos Claros. (s. f.). Qué es y cómo interpretar una regresión logística. Recuperado el 14 de septiembre de 2025, de https://conceptosclaros.com/que-es-regresion-logistica/",
        "OpenAI. (2025). ChatGPT (septiembre 16, [versión GPT-5]). OpenAI. https://chat.openai.com/"
    ]
    # Asegúrate que el nombre del template exista: r_logistica_concepto.html
    return render_template("r_logistica_concepto.html", referencias=referencias, casos=casos, active_page='r_logistica_concepto')

@app.route("/regresion-logistica/ejercicio", methods=["GET", "POST"])
def r_logistica_ejercicio():
    rlog.ensure_model()
    workflow_description = rlog.workflow_description
    descripcion_dataset = rlog.get_dataset_description()

    metrics = rlog.evaluate()
    report_dict = metrics.get("report", {})

    confusion_path = os.path.join(os.path.dirname(__file__), "confusion_matrix.png")
    with open(confusion_path, "rb") as image_file:
        confusion_png = base64.b64encode(image_file.read()).decode("utf-8")

    prediccion = None
    valores = None

    if request.method == "POST":
        try:
            valores = {
                "Study_Time": float(request.form.get("Study_Time")),
                "Number_of_Absences": float(request.form.get("Number_of_Absences")),
                "Final_Grade": float(request.form.get("Final_Grade")),
                "School_Support": request.form.get("School_Support"),
                "Family_Support": request.form.get("Family_Support"),
                "Internet_Access": request.form.get("Internet_Access"),
                "Wants_Higher_Education": request.form.get("Wants_Higher_Education")
            }
            label, prob = rlog.predict_label(valores)
            prediccion = {
                "label": label,
                "probabilidad": f"{prob*100:.6f}%  ({prob:.8e})"
            }
        except (TypeError, ValueError):
            prediccion = {"label": "Error", "probabilidad": "Datos inválidos"}

    return render_template(
        "r_logistica_ejercicio.html",
        workflow_description=workflow_description,
        descripcion_dataset=descripcion_dataset,
        confusion_png=confusion_png,
        report=report_dict,
        prediccion=prediccion,
        valores=valores,
        casos=casos,
        active_page='r_logistica_ejercicio'
    )

# ---------------------------
# CLASIFICACIÓN - CONCEPTOS
# ---------------------------
@app.route("/clasificacion/conceptos")
def clasificacion_conceptos():
    referencias = [
        "Chen, T., & Guestrin, C. (2016). XGBoost: A scalable tree boosting system. In Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining (pp. 785–794).",
        "Pedregosa, F., et al. (2011). Scikit-learn: Machine learning in Python. Journal of Machine Learning Research, 12, 2825–2830.",
        "Fawcett, T. (2006). An introduction to ROC analysis. Pattern Recognition Letters, 27(8), 861–874."
    ]
    return render_template(
        "clasificacion_conceptos.html",
        referencias=referencias,
        casos=casos,
        active_page='clasificacion_conceptos'
    )

# ---------------------------
# CLASIFICACIÓN - EJERCICIO
# ---------------------------
@app.route("/clasificacion/ejercicio", methods=["GET", "POST"])
def clasificacion_ejercicio():
    # Ruta absoluta al CSV
    csv_absoluto = os.path.join(os.path.dirname(__file__), "data", "credit_demo.csv")

    # Entrenar y evaluar el modelo: usa la carpeta estática real de Flask
    metrics = xgb.evaluate(csv_path=csv_absoluto, output_dir=current_app.static_folder)
    report_dict = metrics.get("report", {})
    confusion_filename = metrics.get("confusion_filename")  # acorde a xgb_credit.py corregido

    prediccion = None
    valores = None

    if request.method == "POST":
        try:
            valores = {
                "historial_crediticio": request.form["historial_crediticio"],
                "nivel_endeudamiento": float(request.form["nivel_endeudamiento"]),
                "ingresos_mensuales": float(request.form["ingresos_mensuales"]),
                "edad": float(request.form["edad"]),
                "tipo_empleo": request.form["tipo_empleo"]
            }
            threshold = float(request.form.get("threshold", 0.5))
            prediccion = xgb.predict_label(valores, threshold=threshold)
        except (TypeError, ValueError) as e:
            prediccion = {"label": "Error", "probabilidad": str(e)}

    return render_template(
        "clasificacion_ejercicio.html",
        accuracy=metrics["accuracy"],
        report=report_dict,
        confusion_filename=confusion_filename,
        prediccion=prediccion,
        valores=valores,
        casos=casos,
        active_page='clasificacion_ejercicio'
    )

# ---------------------------
# APRENDIZAJE POR REFUERZO
# ---------------------------
@app.route("/aprendizaje-por-refuerzo/conceptos")
def rl_conceptos():
    referencias = [
        "Sutton, R. S., & Barto, A. G. (2018). Reinforcement learning: An introduction (2nd ed.). MIT Press.",
        "Watkins, C. J. C. H., & Dayan, P. (1992). Q-learning. Machine learning, 8(3-4), 279-292.",
        "Mnih, V., et al. (2015). Human-level control through deep reinforcement learning. Nature, 518(7540), 529-533.",
        "OpenAI. (2023). Spinning Up in Deep RL. https://spinningup.openai.com/en/latest/",
        "DeepMind. (2016). Mastering the game of Go with deep neural networks and tree search. Nature, 529(7587), 484-489."
    ]
    return render_template(
        "rl_conceptos.html", 
        referencias=referencias, 
        casos=casos, 
        active_page='rl_conceptos'
    )

@app.route("/aprendizaje-por-refuerzo/ejercicio", methods=["GET", "POST"])
def rl_ejercicio():
    """Ejercicio práctico de Reinforcement Learning con GridWorld"""
    
    # Estado inicial del entorno
    env_state = rl_module.get_training_status()
    
    # Variables por defecto
    training_plot = None
    simulation_plot = None
    training_result = None
    
    if request.method == "POST":
        action = request.form.get("action")
        
        if action == "train":
            # Obtener parámetros de entrenamiento
            episodes = int(request.form.get("episodes", 100))
            learning_rate = float(request.form.get("learning_rate", 0.1))
            discount_factor = float(request.form.get("discount_factor", 0.9))
            exploration_rate = float(request.form.get("exploration_rate", 1.0))
            exploration_decay = float(request.form.get("exploration_decay", 0.995))
            
            # Entrenar el agente con parámetros personalizados
            training_result = rl_module.train_agent(
                episodes=episodes,
                learning_rate=learning_rate,
                discount_factor=discount_factor,
                exploration_rate=exploration_rate,
                exploration_decay=exploration_decay
            )
            
            # Generar gráfico de entrenamiento actualizado
            training_plot = rl_module.get_training_plots()
            
        elif action == "simulate":
            # Simular un episodio
            simulation_result = rl_module.simulate_episode()
            simulation_plot = simulation_result.get("simulation_plot") if simulation_result else None
    
    # Obtener gráfico de entrenamiento si existe un modelo entrenado
    if not training_plot:
        try:
            training_plot = rl_module.get_training_plots()
        except:
            training_plot = None
    
    return render_template(
        "rl_ejercicio.html",
        env_state=env_state,
        training_plot=training_plot,
        simulation_plot=simulation_plot,
        training_result=training_result,
        casos=casos,
        active_page='rl_ejercicio'
    )

@app.route("/api/rl/train", methods=["POST"])
def api_rl_train():
    """API endpoint para entrenar el agente de RL"""
    try:
        data = request.get_json()
        episodes = data.get("episodes", 100)
        learning_rate = data.get("learning_rate", 0.1)
        discount_factor = data.get("discount_factor", 0.9)
        exploration_rate = data.get("exploration_rate", 1.0)
        exploration_decay = data.get("exploration_decay", 0.995)
        
        # Entrenar el agente con parámetros personalizados
        result = rl_module.train_agent(
            episodes=episodes,
            learning_rate=learning_rate,
            discount_factor=discount_factor,
            exploration_rate=exploration_rate,
            exploration_decay=exploration_decay
        )
        
        return jsonify({
            "success": True,
            "result": result,
            "plot": rl_module.get_training_plots(),
            "metrics": rl_module.get_training_metrics()
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })

@app.route("/api/rl/simulate", methods=["POST"])
def api_rl_simulate():
    """API endpoint para simular un episodio"""
    try:
        result = rl_module.simulate_episode()
        return jsonify({
            "success": True,
            "result": result
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })

@app.route("/api/rl/status")
def api_rl_status():
    """API endpoint para obtener el estado del entorno"""
    try:
        status = rl_module.get_training_status()
        return jsonify({
            "success": True,
            "status": status
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })

@app.route("/api/rl/reset", methods=["POST"])
def api_rl_reset():
    """API endpoint para resetear el agente y empezar desde cero"""
    try:
        result = rl_module.reset_agent()
        return jsonify({
            "success": True,
            "result": result,
            "message": "Agente reseteado exitosamente"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })

@app.route("/api/rl/train-continue", methods=["POST"])
def api_rl_train_continue():
    """API endpoint para continuar entrenamiento del agente actual"""
    try:
        data = request.get_json()
        episodes = data.get("episodes", 100)
        learning_rate = data.get("learning_rate")
        discount_factor = data.get("discount_factor")
        exploration_rate = data.get("exploration_rate")
        exploration_decay = data.get("exploration_decay")
        reset = data.get("reset", False)
        
        # Entrenar el agente (continuo o con reset)
        result = rl_module.train_agent(
            episodes=episodes,
            learning_rate=learning_rate,
            discount_factor=discount_factor,
            exploration_rate=exploration_rate,
            exploration_decay=exploration_decay,
            reset=reset
        )
        
        return jsonify({
            "success": True,
            "result": result,
            "plot": rl_module.get_training_plots(),
            "metrics": rl_module.get_training_metrics()
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })

@app.route("/api/rl/metrics")
def api_rl_metrics():
    """API endpoint para obtener métricas en tiempo real"""
    try:
        metrics = rl_module.get_training_metrics()
        plot = rl_module.get_training_plots()
        return jsonify({
            "success": True,
            "metrics": metrics,
            "plot": plot
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })

# ---------------------------
# MAIN
# ---------------------------
if __name__ == "__main__":
    app.run(debug=True)
