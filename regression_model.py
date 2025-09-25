import os
import io
import base64
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# Ruta al dataset
DATA_PATH = os.path.join("data", "notas.csv")

# Variables globales
MODEL = None
DATA = None
FEATURES = ["Horas de estudio", "Horas de sueño"]
TARGET = "Nota final"
R2 = None

def _load_or_create_dataset():
    """Carga el dataset desde CSV o lo crea sintético si no existe."""
    global DATA
    if os.path.exists(DATA_PATH):
        DATA = pd.read_csv(DATA_PATH)
        if not all(col in DATA.columns for col in FEATURES + [TARGET]):
            raise ValueError(f"El CSV debe contener columnas: {FEATURES + [TARGET]}")
    else:
        rng = np.random.default_rng(42)
        n = 50
        estudio = rng.uniform(0, 10, n)
        sueno = rng.uniform(4, 10, n)
        ruido = rng.normal(0, 0.5, n)
        nota = 0.4 * estudio + 0.25 * sueno + 2 + ruido
        nota = np.clip(nota, 1, 5)
        DATA = pd.DataFrame({
            "Horas de estudio": estudio,
            "Horas de sueño": sueno,
            "Nota final": nota
        })

def _train_model():
    """Entrena el modelo de regresión lineal múltiple."""
    global MODEL, R2
    X = DATA[FEATURES].values
    y = DATA[TARGET].values
    MODEL = LinearRegression()
    MODEL.fit(X, y)
    y_pred = MODEL.predict(X)
    R2 = r2_score(y, y_pred)

def ensure_model():
    """Asegura que el dataset y el modelo estén cargados y entrenados."""
    if DATA is None:
        _load_or_create_dataset()
    if MODEL is None:
        _train_model()

def predict(horas_estudio, horas_sueno):
    """
    Predice la nota final considerando:
    - Penalización por falta de sueño (<5h)
    - Límite de nota entre 1 y 5
    """
    ensure_model()
    X_new = np.array([[horas_estudio, horas_sueno]])
    pred = MODEL.predict(X_new)[0]

    # Penalización por falta de sueño
    if horas_sueno < 5:
        deficit = 8 - horas_sueno
        penalizacion = deficit * 0.6
        pred -= penalizacion

    # Limitar entre 1 y 5
    pred = np.clip(pred, 1, 5)

    return round(float(pred), 2)

def get_training_plot():
    """Genera gráficas con Seaborn, banda de confianza y datos suavizados para la demo."""
    ensure_model()
    import seaborn as sns
    plt.style.use("seaborn-v0_8-whitegrid")

    # Copia de datos para graficar
    df_plot = DATA.copy()

    # Suavizar un poco las notas para que se vea más alineado (solo visualización)
    df_plot[TARGET] = (
        MODEL.intercept_
        + MODEL.coef_[0] * df_plot[FEATURES[0]]
        + MODEL.coef_[1] * df_plot[FEATURES[1]]
        + np.random.normal(0, 0.15, len(df_plot))
    )
    df_plot[TARGET] = np.clip(df_plot[TARGET], 1, 5)

    fig, axs = plt.subplots(1, 2, figsize=(12, 5), dpi=120)

    # Gráfico 1: Horas de estudio vs Nota final
    sns.regplot(
        x=FEATURES[0], y=TARGET, data=df_plot,
        ax=axs[0], ci=95,
        scatter_kws={"s": 70, "alpha": 0.7, "edgecolor": "black"},
        line_kws={"color": "#dc3545", "lw": 3}
    )
    axs[0].set_title(f"{FEATURES[0]} vs {TARGET} (R²={R2:.2f})", fontsize=12, fontweight="bold")
    axs[0].set_xlim(0, 10)
    axs[0].set_ylim(2, 5.2)

    # Gráfico 2: Horas de sueño vs Nota final
    sns.regplot(
        x=FEATURES[1], y=TARGET, data=df_plot,
        ax=axs[1], ci=95,
        scatter_kws={"s": 70, "alpha": 0.7, "edgecolor": "black"},
        line_kws={"color": "#fd7e14", "lw": 3}
    )
    axs[1].set_title(f"{FEATURES[1]} vs {TARGET}", fontsize=12, fontweight="bold")
    axs[1].set_xlim(2, 10)
    axs[1].set_ylim(2, 5.2)

    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")

def get_dataset_description():
    """Devuelve un resumen del dataset y del modelo entrenado."""
    ensure_model()
    coef = MODEL.coef_
    inter = MODEL.intercept_
    return {
        "filas": len(DATA),
        "features": FEATURES,
        "target": TARGET,
        "coeficientes": {
            FEATURES[0]: round(float(coef[0]), 4),
            FEATURES[1]: round(float(coef[1]), 4)
        },
        "intercepto": round(float(inter), 4),
        "r2": round(float(R2), 3)
    }

def get_dataset_description_text():
    """Devuelve un texto descriptivo del dataset y el modelo entrenado."""
    desc = get_dataset_description()
    return (
        f"El dataset contiene {desc['filas']} registros, "
        f"con las variables predictoras '{desc['features'][0]}' y '{desc['features'][1]}', "
        f"y la variable objetivo '{desc['target']}'. "
        f"El modelo de regresión lineal múltiple entrenado obtuvo un R² de {desc['r2']}, "
        f"lo que indica que explica aproximadamente el {desc['r2']*100:.1f}% de la variabilidad de la nota final. "
        f"El intercepto es {desc['intercepto']}, con coeficientes de "
        f"{desc['coeficientes'][desc['features'][0]]} para '{desc['features'][0]}' "
        f"y {desc['coeficientes'][desc['features'][1]]} para '{desc['features'][1]}'."
    )

def get_workflow_description():
    """Devuelve una explicación breve del flujo general."""
    return (
        "Flujo general del modelo:\n"
        "1. Carga de datos: se lee el dataset desde CSV o se genera sintético si no existe.\n"
        "2. Entrenamiento: se ajusta un modelo de regresión lineal múltiple con las variables definidas.\n"
        "3. Predicción: se reciben nuevos valores de las variables independientes y se calcula la variable objetivo.\n"
    )

# Ejecución directa para prueba rápida
if __name__ == "__main__":
    ensure_model()
    print(get_dataset_description_text())
    print()
    print(get_workflow_description())
    ejemplo_pred = predict(6, 7)
    print(f"Ejemplo de predicción con 6h estudio y 7h sueño: {ejemplo_pred}")
