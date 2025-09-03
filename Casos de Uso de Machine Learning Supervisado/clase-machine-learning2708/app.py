from flask import Flask, render_template
app = Flask(__name__)

# casos de uso de machine learning
casos = [
    {
        "id": "netflix",
        "sector": "Entretenimiento",
        "organizacion": "Netflix Inc.",
        "problema": "Recomendación personalizada de contenido",
        "algoritmo": "Filtrado colaborativo supervisado + modelos de clasificación",
        "tarea": "Predicción de preferencia de usuario",
        "datos": "Historial de visualización, calificaciones, metadatos de contenido",
        "metrica": "Precisión de recomendación, tasa de retención",
        "beneficios": "Mejora en la experiencia del usuario, aumento en el tiempo de visualización, reducción del abandono",
        "referencia": [
            "Netflix Research. (2025). *Machine Learning*. https://research.netflix.com/research-area/machine-learning",
            "Marrero, B. (2023). *Netflix y el análisis de datos*. https://beatrizmarrero.com/netflix-y-el-analisis-de-datos",
            "InspiraIA. (2024, diciembre 27). *Machine Learning y Netflix: cómo las recomendaciones personalizadas transformaron el streaming*. https://inspiraia.com/machine-learning/netflix-recomendaciones-personalizadas"
        ]
    },
    {
    "id": "ibmwatson",
    "sector": "Salud",
    "organizacion": "IBM Watson Health",
    "problema": "Diagnóstico asistido en oncología y otras especialidades mediante análisis de datos clínicos e imágenes médicas",
    "algoritmo": "Redes neuronales convolucionales (CNN) y modelos de clasificación supervisados",
    "tarea": "Clasificación de imágenes médicas y apoyo a la decisión clínica",
    "datos": "Historias clínicas electrónicas, resultados de laboratorio, estudios de imagen (radiografías, resonancias, mamografías)",
    "metrica": "Precisión diagnóstica, sensibilidad, especificidad",
    "beneficios": "Mayor rapidez y precisión en el diagnóstico, detección temprana de enfermedades, tratamientos personalizados y apoyo a la investigación médica",
    "referencia": [
        "Rossi, G. (2023, junio 21). IBM Watson Health: Cómo la inteligencia artificial ayuda a la medicina. Vive Virtual. Recuperado el 3 de septiembre de 2025, de https://vivevirtual.es/inteligencia-artificial/ibm-watson-health/#google_vignette",
        "IBM. (s/f). Productos. IBM.com. Recuperado el 3 de septiembre de 2025, de https://www.ibm.com/products"
    ]
    },
    {
        "id": "cocacola",
        "sector": "Consumo masivo",
        "organizacion": "Coca‑Cola Andina",
        "problema": "Optimización logística y predicción de demanda",
        "algoritmo": "Modelos supervisados de predicción de demanda y optimización de rutas",
        "tarea": "Pronóstico de ventas y optimización de distribución",
        "datos": "Historial de ventas, datos de inventario, datos de distribución, variables externas (clima, eventos)",
        "metrica": "Exactitud del pronóstico, tasa de cumplimiento de pedidos",
        "beneficios": "Reducción de quiebres de stock, optimización de inventarios, mejora en la satisfacción del cliente",
        "referencia": [
            "Amazon Web Services. (s/f). Coca‑Cola Andina uses AWS analytics to improve operations. AWS. Recuperado el 3 de septiembre de 2025, de https://aws.amazon.com/es/solutions/case-studies/coca-cola-andina-analytics-case-study/",
            "DigitalDefynd. (2023). 10 ways Coca‑Cola is using Artificial Intelligence. DigitalDefynd.com. Recuperado el 3 de septiembre de 2025, de https://digitaldefynd.com/IQ/ways-coca-cola-uses-artificial-intelligence/"
    ]
    },
    {
        "id": "bancolombia",
        "sector": "Finanzas",
        "organizacion": "Bancolombia",
        "problema": "Detección de fraudes en transacciones",
        "algoritmo": "Modelos de clasificación supervisados (Random Forest, XGBoost)",
        "tarea": "Detección de anomalías",
        "datos": "Historial de transacciones, patrones de comportamiento del usuario",
        "metrica": "Tasa de detección de fraudes, tasa de falsos positivos",
        "beneficios": "Reducción de pérdidas por fraudes, mejora en la seguridad de las transacciones, aumento de la confianza del cliente",
        "referencia": [    
            "Centro de Competencias Inteligencia artificial. (s/f). Bancolombia. Recuperado el 3 de septiembre de 2025, de https://www.bancolombia.com/acerca-de/sala-prensa/noticias/innovacion/centro-de-competencias-inteligencia-artificial",
            "Bancolombia. (s/f). ¿Cuál es el futuro del big data e inteligencia artificial? Bancolombia.com. Recuperado el 3 de septiembre de 2025, de https://blog.bancolombia.com/innovacion/big-data-inteligencia-artificial/?utm_term=smb+manufacturing+software/?wtime=%7Bseek_to_second_number%7D"
            "Bancolombia. (2024). Inteligencia artificial, machine learning, deep learning I Grupo Bancolombia. Bancolombia.com. Recuperado el 3 de septiembre de 2025, de https://blog.bancolombia.com/innovacion/inteligencia-artificial-machine-learning-deep-learning",
        ]
}

]


# Renderiza página principal con lista de casos disponibles
@app.route("/")
def index():
    return render_template("index.html", casos=casos)

# Implementa ruta dinámica para mostrar detalles de cada caso por ID
@app.route("/caso/<id>")
def caso(id):
    c = next((x for x in casos if x["id"] == id), None)
    return render_template("caso.html", caso=c)

if __name__ == "__main__":
    app.run(debug=True)


