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

DATA_PATH = os.path.join("data", "notas.csv")
MODEL = None
DATA = None
FEATURES = ["Horas de estudio", "Horas de sueño"]
TARGET = "Nota final"
R2 = None

def _load_or_create_dataset():
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
    global MODEL, R2
    X = DATA[FEATURES].values
    y = DATA[TARGET].values
    MODEL = LinearRegression()
    MODEL.fit(X, y)
    y_pred = MODEL.predict(X)
    R2 = r2_score(y, y_pred)

def ensure_model():
    if DATA is None:
        _load_or_create_dataset()
    if MODEL is None:
        _train_model()

def predict(horas_estudio, horas_sueno):
    """
    Predice la nota final considerando:
    - Penalización fuerte por falta de sueño (<5h)
    - Límite de nota entre 1 y 5
    """
    ensure_model()
    X_new = np.array([[horas_estudio, horas_sueno]])
    pred = MODEL.predict(X_new)[0]

    # Penalización por falta de sueño
    if horas_sueno < 5:
        # Penalización proporcional: cada hora menos de 8 resta más
        # Si duermes 1h, la penalización es muy alta
        deficit = 8 - horas_sueno
        penalizacion = deficit * 0.6  # factor de impacto
        pred -= penalizacion

    # Limitar entre 1 y 5
    pred = np.clip(pred, 1, 5)

    return round(float(pred), 2)

def get_training_plot():
    ensure_model()
    fig, axs = plt.subplots(1, 2, figsize=(11, 4), dpi=110)

    x_estudio = DATA["Horas de estudio"].values
    y = DATA[TARGET].values
    sueno_mean = DATA["Horas de sueño"].mean()
    y_line1 = MODEL.intercept_ + MODEL.coef_[0] * x_estudio + MODEL.coef_[1] * sueno_mean
    axs[0].scatter(x_estudio, y, s=18, alpha=0.7, label="Datos")
    axs[0].plot(x_estudio, y_line1, color="crimson", lw=2, label="Ajuste con Sueño=media")
    axs[0].set_title(f"Horas de estudio vs {TARGET} (R²={R2:.2f})")
    axs[0].set_xlabel("Horas de estudio")
    axs[0].set_ylabel(TARGET)
    axs[0].legend()

    x_sueno = DATA["Horas de sueño"].values
    estudio_mean = DATA["Horas de estudio"].mean()
    y_line2 = MODEL.intercept_ + MODEL.coef_[0] * estudio_mean + MODEL.coef_[1] * x_sueno
    axs[1].scatter(x_sueno, y, s=18, alpha=0.7, label="Datos")
    axs[1].plot(x_sueno, y_line2, color="seagreen", lw=2, label="Ajuste con Estudio=media")
    axs[1].set_title(f"Horas de sueño vs {TARGET}")
    axs[1].set_xlabel("Horas de sueño")
    axs[1].set_ylabel(TARGET)
    axs[1].legend()

    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")

def get_dataset_description():
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
