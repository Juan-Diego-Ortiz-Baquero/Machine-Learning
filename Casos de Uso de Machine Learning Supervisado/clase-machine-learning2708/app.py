from flask import Flask, render_template
app = Flask(__name__)

# Casos de uso de Machine Learning Supervisado
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
            "InspiraIA. (2024, diciembre 27). *Machine Learning y Netflix: cómo las recomendaciones personalizadas transformaron el streaming*. https://inspiraia.com/machine-learning/netflix-recomendaciones-personalizadas",
            "OpenAI. (2025). ChatGPT (versión GPT-5) [Modelo de lenguaje de IA]. Recuperado el 28 de agosto de 2025, de https://chat.openai.com/"
        ],
        "contenido_html": """
        <h2>🎬 Caso de uso: Recomendación personalizada de contenido — Netflix</h2>

        <h3>Sector y organización</h3>
        <p>Entretenimiento — Netflix Inc.</p>

        <h3>Tipo de algoritmo</h3>
        <p>Filtrado colaborativo supervisado combinado con modelos de clasificación y técnicas de <em>deep learning</em>. Estos algoritmos analizan patrones de comportamiento y preferencias para predecir qué contenido disfrutará más cada usuario.</p>

        <h3>Tarea supervisada</h3>
        <p>Predicción de preferencias de usuario. El sistema se entrena con datos históricos etiquetados (por ejemplo, interacciones positivas o negativas) y se evalúa comparando las predicciones con las elecciones reales de los usuarios.</p>

        <h3>Datos utilizados</h3>
        <ul>
            <li>Historial de visualización: títulos vistos, tiempo de reproducción, pausas y abandonos.</li>
            <li>Calificaciones explícitas: “me gusta” o puntuaciones dadas por el usuario.</li>
            <li>Metadatos de contenido: género, reparto, director, temática, incluso colores predominantes en escenas.</li>
            <li>Información contextual: dispositivo, hora y día de visualización, ubicación geográfica.</li>
        </ul>
        <p>Estos datos permiten construir un perfil detallado de cada usuario y alimentar modelos híbridos que combinan filtrado colaborativo y filtrado basado en contenido.</p>

        <h3>Métrica de evaluación</h3>
        <ul>
            <li><strong>Precisión de recomendación:</strong> porcentaje de sugerencias que el usuario realmente consume.</li>
            <li><strong>Tasa de retención:</strong> porcentaje de usuarios que continúan suscritos gracias a la relevancia del contenido sugerido.</li>
        </ul>

        <h3>Resultados y beneficios</h3>
        <ul>
            <li>Más del 80% del contenido reproducido proviene de recomendaciones personalizadas.</li>
            <li>Mayor satisfacción del usuario y reducción del abandono (<em>churn rate</em>).</li>
            <li>Optimización de la inversión en contenido original, priorizando producciones con alta probabilidad de éxito.</li>
            <li>Experiencia de usuario única: portadas y descripciones adaptadas a cada perfil.</li>
        </ul>

        <h3>Infraestructura y capacidades habilitadoras</h3>
        <p>Netflix Research desarrolla y optimiza modelos de machine learning a gran escala, incluyendo:</p>
        <ul>
            <li><strong>Filtrado colaborativo:</strong> compara hábitos de visualización entre usuarios para sugerir contenido popular entre perfiles similares.</li>
            <li><strong>Filtrado basado en contenido:</strong> recomienda títulos con características similares a los que el usuario ya disfrutó.</li>
            <li><strong>Modelos híbridos:</strong> combinan ambos enfoques para mejorar la precisión.</li>
            <li><strong>Pruebas A/B continuas:</strong> permiten ajustar algoritmos y medir impacto en métricas clave.</li>
            <li><strong>Deep learning:</strong> analiza características intrínsecas del contenido y patrones complejos de consumo.</li>
        </ul>

        <h3>Casos de éxito</h3>
        <ul>
            <li><strong>House of Cards:</strong> producción original cuyo éxito fue anticipado gracias al análisis de datos sobre preferencias de actores, directores y género.</li>
            <li><strong>Contenido local:</strong> adaptación de producciones a mercados específicos como India, Japón o América Latina.</li>
            <li><strong>Optimización de estrenos:</strong> elección de fechas y horarios de lanzamiento para maximizar visualizaciones.</li>
        </ul>

        <h3>Desafíos</h3>
        <ul>
            <li>Evitar sesgos en los algoritmos que limiten la diversidad de recomendaciones.</li>
            <li>Garantizar la privacidad y seguridad de los datos de los usuarios.</li>
            <li>Gestionar la saturación de contenido para no abrumar al usuario.</li>
        </ul>

        <h3>Futuro</h3>
        <ul>
            <li>Uso de IA generativa para crear contenido adaptado a cada usuario.</li>
            <li>Integración con asistentes virtuales y control por voz.</li>
            <li>Predicciones en tiempo real basadas en el estado de ánimo y comportamiento reciente.</li>
        </ul>

        <h3>Referencias en formato APA</h3>
        <ul>
            <li>Marrero, B. (2023). <em>Netflix y el análisis de datos</em>. Recuperado de <a href="https://beatrizmarrero.com/netflix-y-el-analisis-de-datos">Enlace</a></li>
            <li>InspiraIA. (2024, diciembre 27). <em>Machine Learning y Netflix: cómo las recomendaciones personalizadas transformaron el streaming</em>. Recuperado de <a href="https://inspiraia.com/machine-learning/netflix-recomendaciones-personalizadas">Enlace</a></li>
            <li>Netflix Research. (2025). <em>Machine Learning</em>. Recuperado de <a href="https://research.netflix.com/research-area/machine-learning">Enlace</a></li>
            <li>OpenAI. (2025). ChatGPT (versión GPT-5) [Modelo de lenguaje de IA]. Recuperado el 28 de agosto de 2025, de <a href="https://chat.openai.com/">Enlace</a></li>
        </ul>
        """
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
            "IBM. (s/f). Productos. IBM.com. Recuperado el 3 de septiembre de 2025, de https://www.ibm.com/products",
            "OpenAI. (2025). ChatGPT (versión GPT-5) [Modelo de lenguaje de IA]. Recuperado el 28 de agosto de 2025, de https://chat.openai.com/"
    ],
        "contenido_html": """
        <h2>🩺 Caso de uso: Diagnóstico asistido en oncología y otras especialidades — IBM Watson Health</h2>

        <h3>Sector y organización</h3>
        <p>Salud — IBM Watson Health</p>

        <h3>Tipo de algoritmo</h3>
        <p>Redes neuronales convolucionales (CNN) y modelos de clasificación supervisados. Estos algoritmos procesan imágenes médicas y datos clínicos estructurados para identificar patrones asociados a enfermedades, apoyando a los médicos en diagnósticos más rápidos y precisos.</p>

        <h3>Tarea supervisada</h3>
        <p>Clasificación de imágenes médicas y apoyo a la decisión clínica. El sistema se entrena con imágenes etiquetadas por especialistas (enfermedad presente/ausente) y datos clínicos, para luego predecir diagnósticos y sugerir tratamientos basados en evidencia.</p>

        <h3>Datos utilizados</h3>
        <ul>
            <li>Historias clínicas electrónicas.</li>
            <li>Resultados de laboratorio.</li>
            <li>Estudios de imagen: radiografías, resonancias magnéticas, mamografías.</li>
        </ul>
        <p>La plataforma combina datos estructurados y no estructurados, aplicando procesamiento de lenguaje natural (NLP) para interpretar notas médicas y reportes clínicos.</p>

        <h3>Métrica de evaluación</h3>
        <ul>
            <li><strong>Precisión diagnóstica:</strong> porcentaje de diagnósticos correctos frente a la referencia de especialistas.</li>
            <li><strong>Sensibilidad:</strong> capacidad para detectar casos positivos reales.</li>
            <li><strong>Especificidad:</strong> capacidad para descartar correctamente casos negativos.</li>
        </ul>

        <h3>Resultados y beneficios</h3>
        <ul>
            <li>Diagnósticos más rápidos y precisos en oncología, cardiología y otras especialidades.</li>
            <li>Detección temprana de enfermedades raras y complejas.</li>
            <li>Tratamientos personalizados basados en el perfil clínico del paciente.</li>
            <li>Apoyo a la investigación médica mediante análisis de grandes volúmenes de datos.</li>
            <li>Reducción de costos y mejora de la eficiencia hospitalaria.</li>
        </ul>

        <h3>Casos de éxito</h3>
        <ul>
            <li><strong>Oncología:</strong> IBM Watson for Oncology, en colaboración con el Memorial Sloan Kettering Cancer Center, alcanzó un 90% de concordancia con diagnósticos de especialistas en cáncer de pulmón.</li>
            <li><strong>Pediatría:</strong> detección temprana de enfermedades raras en el Hospital de Niños de Boston, identificando casos que habían pasado desapercibidos.</li>
            <li><strong>Gestión hospitalaria:</strong> reducción de readmisiones innecesarias en el Centro Médico de la Universidad de Carolina del Norte mediante análisis predictivo.</li>
        </ul>

        <h3>Infraestructura y capacidades habilitadoras</h3>
        <p>IBM Watson Health integra múltiples soluciones de IBM, incluyendo:</p>
        <ul>
            <li><strong>IBM Watson Assistant:</strong> interacción conversacional con pacientes y profesionales.</li>
            <li><strong>IBM Watson Studio:</strong> desarrollo y entrenamiento de modelos de IA.</li>
            <li><strong>IBM Cloud Pak for Data:</strong> integración y análisis de datos a gran escala.</li>
            <li><strong>IBM Watson Text to Speech:</strong> accesibilidad y comunicación multicanal.</li>
        </ul>

        <h3>Desafíos y consideraciones éticas</h3>
        <ul>
            <li>Garantizar la privacidad de los datos de los pacientes mediante cifrado y control de acceso.</li>
            <li>Transparencia en los algoritmos y decisiones clínicas asistidas por IA.</li>
            <li>Colaboración con expertos en ética médica y legal para un uso responsable.</li>
        </ul>

        <h3>Futuro</h3>
        <p>Se espera que IBM Watson Health amplíe su alcance a más especialidades médicas, integrando IA generativa para análisis de casos complejos y potenciando la medicina preventiva mediante predicciones personalizadas.</p>

        <h3>Referencias en formato APA</h3>
        <ul>
            <li>Rossi, G. (2023, junio 21). <em>IBM Watson Health: Cómo la inteligencia artificial ayuda a la medicina</em>. Vive Virtual. Recuperado de <a href="https://vivevirtual.es/inteligencia-artificial/ibm-watson-health/#google_vignette">Enlace</a></li>
            <li>IBM. (s/f). <em>Productos</em>. IBM.com. Recuperado de <a href="https://www.ibm.com/products">Enlace</a></li>
            <li>OpenAI. (2025). ChatGPT (versión GPT-5) [Modelo de lenguaje de IA]. Recuperado el 28 de agosto de 2025, de <a href="https://chat.openai.com/">Enlace</a></li>   
        </ul>
        """
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
            "DigitalDefynd. (2023). 10 ways Coca‑Cola is using Artificial Intelligence. DigitalDefynd.com. Recuperado el 3 de septiembre de 2025, de https://digitaldefynd.com/IQ/ways-coca-cola-uses-artificial-intelligence/",
            "OpenAI. (2025). ChatGPT (versión GPT-5) [Modelo de lenguaje de IA]. Recuperado el 28 de agosto de 2025, de https://chat.openai.com/"
    ],
        "contenido_html": """
        <h2>🥤 Caso de uso: Optimización logística y predicción de demanda — Coca‑Cola Andina</h2>

        <h3>Sector y organización</h3>
        <p>Consumo masivo — Coca‑Cola Andina</p>

        <h3>Tipo de algoritmo</h3>
        <p>Modelos supervisados de predicción de demanda y optimización de rutas. Estos modelos analizan datos históricos y variables externas para anticipar la demanda y optimizar la distribución, reduciendo costos y mejorando la eficiencia operativa.</p>

        <h3>Tarea supervisada</h3>
        <p>Pronóstico de ventas y optimización de distribución. El modelo se entrena con datos históricos etiquetados con la demanda real observada, permitiendo predecir volúmenes futuros y ajustar rutas de entrega.</p>

        <h3>Datos utilizados</h3>
        <ul>
            <li>Historial de ventas por región y canal.</li>
            <li>Datos de inventario y niveles de stock en centros de distribución.</li>
            <li>Información de distribución y logística (rutas, tiempos de entrega, capacidad de camiones).</li>
            <li>Variables externas como clima, eventos y promociones.</li>
        </ul>
        <p>Con la solución en AWS, Coca‑Cola Andina actualiza sus datos cada 15 minutos, mejorando la visibilidad de inventarios y operaciones en tiempo casi real.</p>

        <h3>Métrica de evaluación</h3>
        <ul>
            <li><strong>Exactitud del pronóstico:</strong> capacidad del modelo para predecir la demanda real.</li>
            <li><strong>Tasa de cumplimiento de pedidos:</strong> porcentaje de pedidos entregados completos y a tiempo.</li>
        </ul>

        <h3>Resultados y beneficios</h3>
        <ul>    
            <li>1% de aumento en la tasa de cumplimiento de pedidos.</li>
            <li>0,2% de reducción en la tasa de falta de existencias.</li>
            <li>0,3% de reducción en pedidos no recibidos.</li>
            <li>Duplicación del número de unidades de almacenamiento gestionadas.</li>
            <li>Optimización de rutas de entrega, reduciendo costos y emisiones.</li>
            <li>Mayor satisfacción del cliente gracias a entregas más confiables.</li>
        </ul>

        <h3>Infraestructura y capacidades habilitadoras</h3>
        <p>Coca‑Cola Andina migró a un lago de datos en Amazon Web Services (AWS) y desarrolló la aplicación interna <em>Thanos</em> para gestionar inventario, distribución y entregas. Entre las tecnologías utilizadas destacan:</p>
        <ul>
            <li><strong>Amazon S3:</strong> almacenamiento escalable para datos operativos y logísticos.</li>
            <li><strong>Amazon RDS:</strong> gestión de bases de datos relacionales.</li>
            <li><strong>AWS Lambda:</strong> análisis y generación de información en tiempo casi real.</li>
            <li><strong>Amazon SageMaker:</strong> entrenamiento y despliegue de modelos de machine learning para predicción de demanda y optimización logística.</li>
        </ul>
        <p>Además, Coca‑Cola Andina utiliza modelos de machine learning para predecir la disponibilidad de clientes en el momento de la entrega, reduciendo intentos fallidos.</p>

        <h3>Innovaciones con IA</h3>
        <ul>
            <li>Optimización de la cadena de suministro mediante análisis predictivo.</li>
            <li>Personalización de campañas de marketing y promociones según patrones de consumo.</li>
            <li>Integración de IA en mantenimiento predictivo de equipos y flota.</li>
        </ul>

        <h3>Referencias en formato APA</h3>
        <ul>
            <li>Amazon Web Services. (s/f). Coca‑Cola Andina uses AWS analytics to improve operations. AWS. Recuperado el 3 de septiembre de 2025, de <a href="https://aws.amazon.com/es/solutions/case-studies/coca-cola-andina-analytics-case-study">Enlace</a></li>
            <li>DigitalDefynd. (2023). 10 ways Coca‑Cola is using Artificial Intelligence. DigitalDefynd.com. Recuperado el 3 de septiembre de 2025, de <a href="https://digitaldefynd.com/IQ/ways-coca-cola-uses-artificial-intelligence">Enlace</a></li>
            <li>OpenAI. (2025). ChatGPT (versión GPT-5) [Modelo de lenguaje de IA]. Recuperado el 28 de agosto de 2025, de <a href="https://chat.openai.com/">Enlace</a></li>
        </ul>
        """
},
    {
        "id": "bancolombia",
        "sector": "Finanzas",
        "organizacion": "Bancolombia",
        "problema": "Detección de fraudes en transacciones",
        "algoritmo": "Modelos de clasificación supervisados (Random Forest, XGBoost)",
        "tarea": "Clasificación binaria (fraude vs. legítima)",
        "datos": "Historial de transacciones, patrones de comportamiento del usuario",
        "metrica": "Tasa de detección de fraudes, tasa de falsos positivos",
        "beneficios": "Reducción de pérdidas por fraudes, mejora en la seguridad de las transacciones, aumento de la confianza del cliente",
        "referencia": [    
            "Centro de Competencias Inteligencia artificial. (s/f). Bancolombia. Recuperado el 3 de septiembre de 2025, de https://www.bancolombia.com/acerca-de/sala-prensa/noticias/innovacion/centro-de-competencias-inteligencia-artificial",
            "Bancolombia. (s/f). ¿Cuál es el futuro del big data e inteligencia artificial? Bancolombia.com. Recuperado el 3 de septiembre de 2025, de https://blog.bancolombia.com/innovacion/big-data-inteligencia-artificial/?utm_term=smb+manufacturing+software/?wtime=%7Bseek_to_second_number%7D",
            "Bancolombia. (2024). Inteligencia artificial, machine learning, deep learning I Grupo Bancolombia. Bancolombia.com. Recuperado el 3 de septiembre de 2025, de https://blog.bancolombia.com/innovacion/inteligencia-artificial-machine-learning-deep-learning",
            "OpenAI. (2025). ChatGPT (versión GPT-5) [Modelo de lenguaje de IA]. Recuperado el 28 de agosto de 2025, de https://chat.openai.com/"
        ],
        "contenido_html": """
<h2>🏦 Caso de uso: Detección de fraudes en transacciones — Bancolombia</h2>

<h3>Sector y organización</h3>
<p>Finanzas — Bancolombia</p>

<h3>Tipo de algoritmo</h3>
<p>Modelos de clasificación supervisados como Random Forest y XGBoost. Según Bancolombia, estos modelos se enmarcan dentro del <em>Machine Learning</em> (aprendizaje automático), que es una rama de la Inteligencia Artificial. En este enfoque, el sistema aprende a partir de datos históricos etiquetados (transacciones legítimas vs. fraudulentas) para identificar patrones y predecir si una nueva transacción es sospechosa.</p>

<h3>Tarea supervisada</h3>
<p>Detección de anomalías en operaciones financieras. Aunque la tarea se describe como “detección de anomalías”, en este contexto se implementa como un problema de clasificación binaria supervisada:</p>
<ul>
<li>Clase 1: Transacción fraudulenta</li>
<li>Clase 0: Transacción legítima</li>
</ul>

<h3>Datos utilizados</h3>
<ul>
<li>Historial de transacciones (monto, hora, ubicación, canal de pago, dispositivo usado).</li>
<li>Patrones de comportamiento del usuario (frecuencia de compras, comercios habituales, geolocalización).</li>
<li>Variables derivadas (por ejemplo, diferencia entre ubicación habitual y ubicación actual).</li>
</ul>
<p>Aquí entra en juego el Big Data: Bancolombia procesa grandes volúmenes de datos en tiempo real para alimentar los modelos de IA. Según su blog sobre Big Data e Inteligencia Artificial, la combinación de ambas tecnologías permite analizar millones de registros en segundos, detectar correlaciones y generar alertas inmediatas.</p>

<h3>Métrica de evaluación</h3>
<ul>
<li><strong>Tasa de detección de fraudes (Recall o Sensibilidad):</strong> porcentaje de fraudes detectados sobre el total real de fraudes.</li>
<li><strong>Tasa de falsos positivos:</strong> porcentaje de transacciones legítimas que fueron marcadas erróneamente como fraude.</li>
</ul>
<p>El objetivo es maximizar la detección sin incomodar al cliente con bloqueos innecesarios.</p>

<h3>Resultados y beneficios</h3>
<ul>
<li>Reducción de pérdidas económicas por fraudes.</li>
<li>Mejora en la seguridad de las transacciones.</li>
<li>Aumento de la confianza del cliente en los canales digitales.</li>
<li>Procesos de validación más rápidos y menos intrusivos.</li>
</ul>

<h3>Infraestructura y capacidades habilitadoras</h3>
<p>El Centro de Competencias en Inteligencia Artificial de Bancolombia es clave para este tipo de proyectos. Allí trabajan con aliados como IBM, Microsoft y Cognitiva para aplicar:</p>
<ul>
<li><strong>Procesamiento de Lenguaje Natural (NLP):</strong> para interpretar descripciones de transacciones o interacciones con clientes.</li>
<li><strong>Reconocimiento de patrones y anomalías</strong> con Machine Learning y Deep Learning.</li>
<li><strong>Visión por computador:</strong> útil en otros casos, como verificación de identidad por documentos o biometría.</li>
<li><strong>Planificación y razonamiento:</strong> para priorizar alertas y decidir acciones automáticas.</li>
</ul>
<p>Este centro también entrena modelos continuamente, incorporando nuevos datos y adaptándose a tácticas emergentes de fraude.</p>

<h3>Referencias en formato APA</h3>
<ul>
<li>Bancolombia. (2024, 8 de mayo). Inteligencia artificial, machine learning, deep learning: ¿son sinónimos? <a href="https://blog.bancolombia.com/innovacion/inteligencia-artificial-machine-learning-deep-learning">Enlace</a></li>
<li>Bancolombia. (s.f.). Big Data e Inteligencia Artificial. <a href="https://blog.bancolombia.com/innovacion/big-data-inteligencia-artificial">Enlace</a></li>
<li>Bancolombia. (2018, 26 de abril). Centro de Competencias en Inteligencia Artificial. <a href="https://www.bancolombia.com/acerca-de/sala-prensa/noticias/innovacion/centro-de-competencias-inteligencia-artificial">Enlace</a></li>
<li>OpenAI. (2025). ChatGPT (versión GPT-5) [Modelo de lenguaje de IA]. Recuperado el 28 de agosto de 2025, de <a href="https://chat.openai.com/">Enlace</a></li>
</ul>
"""
    }
]

@app.route("/")
def index():
    return render_template("index.html", casos=casos)

@app.route("/caso/<id>")
def caso(id):
    c = next((x for x in casos if x["id"] == id), None)
    return render_template("caso.html", caso=c)

if __name__ == "__main__":
    app.run(debug=True)
# Para ejecutar la aplicación, guarda este archivo como app.py y ejecuta: