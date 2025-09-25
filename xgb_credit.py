# xgb_credit.py
# Caso práctico: Otorgamiento de crédito con XGBoost
# Autor: Juan Diego Ortiz Baquero

import os
from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

from xgboost import XGBClassifier

# ----------------------------
# Configuración
# ----------------------------
RANDOM_STATE = 42
NUMERIC_FEATURES = ["nivel_endeudamiento", "ingresos_mensuales", "edad"]
CATEGORICAL_FEATURES = ["historial_crediticio", "tipo_empleo"]
TARGET_COLUMN = "aprobacion"

MODEL_PIPELINE = None
TRAIN_COLUMNS = None


def _resolve_static_folder(output_dir: str | None) -> str:
    """
    Resuelve la carpeta estática real de Flask para guardar archivos.
    Si no hay app activa o no se pasa output_dir, cae al 'static' junto a este archivo.
    """
    if output_dir:
        return output_dir

    # Intenta usar la carpeta estática de Flask
    try:
        from flask import current_app
        if current_app and current_app.static_folder:
            return current_app.static_folder
    except Exception:
        pass

    # Fallback: 'static' al lado de este archivo (evita crear otra static en cwd)
    return str(Path(__file__).parent / "static")


# ----------------------------
# Función principal de evaluación
# ----------------------------
def evaluate(csv_path: str = "data/credit_demo.csv", output_dir: str | None = None, test_size: float = 0.2):
    """
    Entrena y evalúa el modelo XGBoost.
    Retorna métricas y guarda imagen de matriz de confusión dentro de la carpeta estática real.
    """
    global MODEL_PIPELINE, TRAIN_COLUMNS

    static_dir = _resolve_static_folder(output_dir)
    os.makedirs(static_dir, exist_ok=True)

    # Cargar dataset
    df = pd.read_csv(csv_path)
    # Mapeo de clase positiva
    df[TARGET_COLUMN] = df[TARGET_COLUMN].map({"Sí": 1, "No": 0})

    X = df[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
    y = df[TARGET_COLUMN]

    # Split con estratificación
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=RANDOM_STATE, stratify=y
    )

    # Preprocesamiento
    numeric_transformer = SimpleImputer(strategy="median")
    categorical_transformer = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore"))
    ])

    preprocessor = ColumnTransformer([
        ("num", numeric_transformer, NUMERIC_FEATURES),
        ("cat", categorical_transformer, CATEGORICAL_FEATURES)
    ])

    # Modelo XGBoost
    model = XGBClassifier(
        n_estimators=300,
        max_depth=4,
        learning_rate=0.08,
        subsample=0.9,
        colsample_bytree=0.9,
        random_state=RANDOM_STATE,
        n_jobs=-1
    )

    # Pipeline completo
    MODEL_PIPELINE = Pipeline([
        ("preprocessor", preprocessor),
        ("model", model)
    ])

    # Entrenar
    MODEL_PIPELINE.fit(X_train, y_train)
    TRAIN_COLUMNS = list(X.columns)

    # Predicciones
    y_pred = MODEL_PIPELINE.predict(X_test)

    # Métricas
    acc = round(accuracy_score(y_test, y_pred), 4)
    report = classification_report(y_test, y_pred, output_dict=True)
    cm = confusion_matrix(y_test, y_pred)

    # Guardar matriz de confusión como imagen dentro del static correcto
    confusion_filename = "confusion_xgb.png"
    confusion_path = os.path.join(static_dir, confusion_filename)

    plt.figure(figsize=(5, 4))
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=["Pred 0", "Pred 1"],
        yticklabels=["Real 0", "Real 1"],
    )
    plt.title("Matriz de confusión — XGBoost")
    plt.ylabel("Reales")
    plt.xlabel("Predichos")
    plt.tight_layout()
    plt.savefig(confusion_path)
    plt.close()

    return {
        "accuracy": acc,
        "report": report,
        "confusion_filename": confusion_filename  # devuelve solo el nombre para url_for('static', filename=...)
    }


# ----------------------------
# Función de predicción
# ----------------------------
def predict_label(features: dict, threshold: float = 0.5):
    """
    Predice etiqueta “Sí”/“No” y probabilidad asociada para un registro.
    Requiere que evaluate() haya sido llamado antes para entrenar y preparar el pipeline.
    """
    if MODEL_PIPELINE is None or TRAIN_COLUMNS is None:
        raise RuntimeError("Primero llama a evaluate() para entrenar el modelo.")

    if not (0.0 <= threshold <= 1.0):
        raise ValueError("El threshold debe estar entre 0 y 1.")

    # Validar campos requeridos
    required = NUMERIC_FEATURES + CATEGORICAL_FEATURES
    missing = [f for f in required if f not in features]
    if missing:
        raise ValueError(f"Faltan campos requeridos: {missing}")

    # Armar DataFrame de una fila (manteniendo el orden de columnas)
    row = {col: features[col] for col in required}
    X_new = pd.DataFrame([row], columns=required)

    # Probabilidad de clase positiva
    proba_pos = float(MODEL_PIPELINE.predict_proba(X_new)[:, 1][0])

    # Depuración (opcional): deja activo mientras pruebas
    print(f"[DEBUG] Features: {row}")
    print(f"[DEBUG] Threshold recibido: {threshold}")
    print(f"[DEBUG] Probabilidad calculada: {proba_pos}")

    label = "Sí" if proba_pos >= threshold else "No"

    msg = (
        f"Con threshold={threshold:.2f}, si reduces el umbral aumentas la sensibilidad "
        f"(Recall) pero puedes bajar la precisión; si lo aumentas, ocurrirá lo contrario."
    )

    return {
        "label": label,
        "probabilidad": round(proba_pos, 4),
        "threshold": round(threshold, 2),
        "umbral_msg": msg,
    }
