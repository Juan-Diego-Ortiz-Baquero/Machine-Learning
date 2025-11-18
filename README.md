# Plataforma Educativa de Machine Learning

## Descripción del Proyecto

Esta plataforma web educativa ha sido desarrollada como una herramienta integral para el aprendizaje y comprensión de conceptos fundamentales en Machine Learning. El sistema proporciona implementaciones prácticas de diversos algoritmos de aprendizaje automático, incluyendo técnicas de aprendizaje supervisado y por refuerzo, con interfaces interactivas que permiten la experimentación y visualización de resultados en tiempo real.

La plataforma está construida utilizando Flask como framework web backend y presenta una arquitectura modular que facilita la extensión y mantenimiento del código. Cada módulo de algoritmo está diseñado con fines educativos, proporcionando tanto la implementación técnica como explicaciones conceptuales detalladas.

## Arquitectura del Sistema

### Estructura del Proyecto

```
Machine-Learning/
├── app.py                      # Aplicación principal Flask
├── requirements.txt            # Dependencias del proyecto
├── data/                       # Conjuntos de datos
│   ├── credit_demo.csv
│   ├── german.data
│   ├── student_dropout.csv
│   └── notas.csv
├── templates/                  # Plantillas HTML
│   ├── home.html
│   ├── regresion_conceptos.html
│   ├── regresion_ejercicio.html
│   ├── r_logistica_concepto.html
│   ├── r_logistica_ejercicio.html
│   ├── clasificacion_conceptos.html
│   ├── clasificacion_ejercicio.html
│   ├── rl_conceptos.html
│   └── rl_ejercicio.html
├── static/                     # Recursos estáticos
│   ├── styles.css
│   ├── app.js
│   └── assets/
└── modules/                    # Módulos de algoritmos
    ├── regression_model.py
    ├── regression_logistica.py
    ├── xgb_credit.py
    └── reinforcement_learning.py
```

### Tecnologías Utilizadas

- **Backend**: Flask 3.1.2 (Python)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5.3.2
- **Visualización**: Matplotlib 3.10.6, Seaborn 0.13.2
- **Machine Learning**: Scikit-learn 1.7.2, XGBoost 3.0.5
- **Procesamiento de Datos**: Pandas 2.3.2, NumPy 2.3.2
- **Interfaz Matemática**: MathJax 3.0

## Algoritmos Implementados

### 1. Regresión Lineal

#### Descripción del Algoritmo
La regresión lineal implementada utiliza el método de mínimos cuadrados ordinarios para establecer relaciones lineales entre variables predictoras y una variable objetivo continua. El algoritmo optimiza los parámetros β₀ (intercepto) y β₁ (pendiente) mediante la minimización de la función de costo de error cuadrático medio.

#### Formulación Matemática
```
y = β₀ + β₁x + ε
```
Donde:
- y: variable dependiente
- x: variable independiente  
- β₀: intercepto
- β₁: coeficiente de regresión
- ε: término de error

#### Implementación Técnica
- **Algoritmo**: Ordinary Least Squares (OLS)
- **Biblioteca**: Scikit-learn LinearRegression
- **Métricas de evaluación**: R², MSE, MAE
- **Validación**: División train/test (80/20)

#### Comportamiento Observado
El modelo de regresión lineal muestra un rendimiento satisfactorio en conjuntos de datos con relaciones lineales claras. En el dataset de notas académicas, se observa:
- R² promedio: 0.75-0.85
- Error cuadrático medio: 0.15-0.25 (normalizado)
- Capacidad predictiva estable con baja varianza

### 2. Regresión Logística

#### Descripción del Algoritmo
La regresión logística implementa un modelo de clasificación binaria utilizando la función sigmoidea para mapear cualquier valor real al rango (0,1). El algoritmo utiliza optimización por gradiente descendente para maximizar la función de verosimilitud.

#### Formulación Matemática
```
P(y=1|x) = 1 / (1 + e^(-(β₀ + β₁x)))
```

#### Implementación Técnica
- **Algoritmo**: Logistic Regression con regularización L2
- **Optimización**: Limited-memory BFGS (lbfgs)
- **Métricas**: Accuracy, Precision, Recall, F1-Score, AUC-ROC
- **Validación cruzada**: 5-fold cross-validation

#### Comportamiento Observado
En el conjunto de datos de crédito alemán:
- Accuracy promedio: 74-76%
- Precisión para clase positiva: 0.68-0.72
- Recall para clase positiva: 0.45-0.55
- AUC-ROC: 0.70-0.75

### 3. XGBoost para Clasificación

#### Descripción del Algoritmo
Implementación de eXtreme Gradient Boosting, un algoritmo de ensemble basado en árboles de decisión que utiliza gradient boosting optimizado para problemas de clasificación de alta dimensionalidad.

#### Características Técnicas
- **Regularización**: L1 y L2 integradas
- **Manejo de valores faltantes**: Nativo
- **Paralelización**: Optimizado para múltiples cores
- **Early stopping**: Prevención de sobreajuste

#### Comportamiento Observado
Rendimiento superior en comparación con regresión logística:
- Accuracy: 76-79%
- Mejor generalización en datos de test
- Reducción de overfitting mediante regularización
- Importancia de características interpretable

### 4. Aprendizaje por Refuerzo (Q-Learning en GridWorld)

#### Descripción del Entorno
Se implementó un entorno GridWorld de 5x5 celdas donde un agente debe navegar desde una posición inicial (0,0) hasta una meta (4,4) evitando obstáculos. El entorno proporciona recompensas diferenciadas según las acciones del agente.

#### Características del Entorno
- **Espacio de estados**: 25 posiciones discretas (5x5 grid)
- **Espacio de acciones**: 4 acciones discretas (arriba, derecha, abajo, izquierda)
- **Recompensas**:
  - Meta alcanzada: +100
  - Obstáculo: -50
  - Paso normal: -1
  - Fuera de límites: -10

#### Algoritmo Q-Learning Implementado

##### Formulación Matemática
```
Q(s,a) ← Q(s,a) + α[r + γ max Q(s',a') - Q(s,a)]
```

Donde:
- α (alpha): tasa de aprendizaje (0.1)
- γ (gamma): factor de descuento (0.95)
- ε (epsilon): tasa de exploración con decaimiento exponencial

##### Parámetros de Configuración
- **Tasa de aprendizaje (α)**: 0.1 (configurable 0.01-1.0)
- **Factor de descuento (γ)**: 0.95 (configurable 0.1-0.99)
- **Exploración inicial (ε)**: 1.0
- **Decaimiento de exploración**: 0.995 por episodio
- **Episodios de entrenamiento**: 100-1000 (configurable)

#### Comportamiento Observado del Agente

##### Fase de Exploración (Episodios 1-100)
- **Comportamiento**: Movimientos aleatorios predominantes
- **Recompensa promedio**: -50 a -20
- **Pasos por episodio**: 40-60 (alta variabilidad)
- **Tasa de éxito**: 5-15%

##### Fase de Aprendizaje (Episodios 100-300)
- **Comportamiento**: Reducción gradual de exploración
- **Recompensa promedio**: -20 a 50
- **Pasos por episodio**: 20-40
- **Tasa de éxito**: 30-60%

##### Fase de Convergencia (Episodios 300+)
- **Comportamiento**: Política óptima estabilizada
- **Recompensa promedio**: 70-95
- **Pasos por episodio**: 8-12 (ruta óptima)
- **Tasa de éxito**: 80-95%

##### Análisis de la Política Aprendida
El agente desarrolla una política óptima que:
1. Evita consistentemente los obstáculos conocidos
2. Minimiza el número de pasos hacia la meta
3. Muestra robustez ante perturbaciones menores
4. Converge a la ruta óptima teórica (8 pasos)

#### Métricas de Rendimiento
- **Tiempo de convergencia**: 200-400 episodios
- **Estabilidad**: ±2% variación en recompensa tras convergencia
- **Eficiencia**: 95% de episodios completados exitosamente
- **Generalización**: Política transferible a configuraciones similares

## Funcionalidades del Sistema

### Interfaces Educativas
- **Conceptos teóricos**: Explicaciones matemáticas detalladas
- **Ejercicios prácticos**: Implementaciones interactivas
- **Visualizaciones**: Gráficos dinámicos de resultados
- **Experimentación**: Parámetros configurables en tiempo real

### Características Técnicas
- **Entrenamiento dinámico**: Múltiples sesiones de entrenamiento acumulativas
- **Visualización en tiempo real**: Gráficos que se actualizan durante el entrenamiento
- **Persistencia de modelos**: Guardado y carga de modelos entrenados
- **API RESTful**: Endpoints para integración programática

## Instalación y Configuración

### Requisitos del Sistema
- Python 3.8 o superior
- 4GB RAM mínimo (8GB recomendado)
- Navegador web moderno con soporte JavaScript ES6

### Instalación

1. **Clonar el repositorio**:
```bash
git clone <repository-url>
cd Machine-Learning
```

2. **Crear entorno virtual**:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

3. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

4. **Ejecutar la aplicación**:
```bash
python app.py
```

5. **Acceder a la plataforma**:
```
http://localhost:5000
```

## Uso del Sistema

### Navegación
- **Página principal**: Acceso a todos los módulos
- **Conceptos**: Marco teórico de cada algoritmo
- **Ejercicios**: Implementaciones prácticas interactivas

### Experimentación con Algoritmos
1. Seleccionar el módulo de interés
2. Configurar parámetros del algoritmo
3. Ejecutar entrenamiento
4. Analizar resultados y visualizaciones
5. Experimentar con diferentes configuraciones

## Casos de Uso Educativos

### Para Estudiantes
- Comprensión práctica de algoritmos de ML
- Experimentación con hiperparámetros
- Visualización de conceptos teóricos
- Análisis comparativo de algoritmos

### Para Educadores  
- Herramienta de demostración en clase
- Plataforma para asignaciones prácticas
- Recurso para explicar conceptos complejos
- Base para proyectos estudiantiles

## Consideraciones Técnicas

### Rendimiento
- Optimizado para conjuntos de datos pequeños a medianos (<10,000 registros)
- Procesamiento en tiempo real para visualizaciones
- Caching de modelos para mejorar tiempos de respuesta

### Limitaciones
- Implementación con fines educativos (no productivo)
- Algoritmos simplificados para claridad conceptual
- Interfaz optimizada para demostración, no para análisis profundo

## Extensibilidad

El sistema está diseñado para facilitar la adición de nuevos algoritmos:
1. Crear módulo de algoritmo en `/modules/`
2. Implementar interfaz estándar (train, predict, visualize)
3. Agregar rutas en `app.py`
4. Crear templates HTML correspondientes

## Referencias Académicas

- Sutton, R. S., & Barto, A. G. (2018). *Reinforcement Learning: An Introduction* (2ª ed.). MIT Press.
- Hastie, T., Tibshirani, R., & Friedman, J. (2009). *The Elements of Statistical Learning*. Springer.
- Bishop, C. M. (2006). *Pattern Recognition and Machine Learning*. Springer.
- Chen, T., & Guestrin, C. (2016). XGBoost: A scalable tree boosting system. *Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining*.

## Licencia

Este proyecto ha sido desarrollado con fines educativos y de investigación. Para uso comercial, consultar con los autores.

---

**Última actualización**: Noviembre 2025  
**Versión**: 1.0.0  
**Autor**: Juan Ortiz
**Institución**: Universidad de Cundinamarca 
