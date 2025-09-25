import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.preprocessing import StandardScaler

# -------------------------------------------------------
# Carga del dataset
# -------------------------------------------------------
base_dir = os.path.abspath(os.path.dirname(__file__))
ruta_csv = os.path.join(base_dir, 'data', 'student_dropout.csv')

if not os.path.exists(ruta_csv):
    raise FileNotFoundError(f"Archivo no encontrado: {ruta_csv}")

data = pd.read_csv(ruta_csv)
if data.empty or data.shape[1] < 2:
    raise ValueError("El archivo CSV está vacío o mal estructurado.")

# -------------------------------------------------------
# Selección de variables
# -------------------------------------------------------
# Variables adaptadas al dataset real
features = [
    'Study_Time',               # Horas de estudio
    'Number_of_Absences',       # Usada como aproximación a 'Asistencia'
    'Final_Grade',              # Reemplazo de 'Promedio académico'
    'School_Support',           # Reemplazo de 'Carrera' (categórica) por variable relevante disponible
    'Family_Support',           # Apoyo familiar
    'Internet_Access',          # Acceso a internet
    'Wants_Higher_Education'    # Deseo de educación superior
]
target = 'Dropped_Out'

X = data[features].copy()
y = data[target].astype(int)  # Convertir True/False a 1/0

# Codificación de variables categóricas tipo yes/no
X = X.replace({'yes': 1, 'no': 0, 'Yes': 1, 'No': 0, True: 1, False: 0})

# -------------------------------------------------------
# División de datos
# -------------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# Escalado
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# -------------------------------------------------------
# Entrenamiento
# -------------------------------------------------------
model = LogisticRegression()
model.fit(X_train_scaled, y_train)

# -------------------------------------------------------
# Evaluación
# -------------------------------------------------------
def evaluate():
    y_pred = model.predict(X_test_scaled)
    acc = accuracy_score(y_test, y_pred)
    matrix = confusion_matrix(y_test, y_pred)
    report = classification_report(y_test, y_pred, target_names=['No', 'Sí'], output_dict=False)

    # Mostrar métricas en consola
    print("\n=== Evaluación del modelo ===")
    print(f"Exactitud (accuracy): {acc:.4f}")
    print("\nReporte de clasificación:")
    print(classification_report(y_test, y_pred, target_names=['No', 'Sí']))
    print("Matriz de confusión (filas = reales, columnas = predichos):")
    print(matrix)

    # Guardar matriz de confusión como imagen
    plt.figure(figsize=(6, 4))
    sns.heatmap(matrix, 
                annot=True, 
                fmt='d', 
                cmap='Blues', 
                cbar=True,
                xticklabels=['No', 'Sí'], 
                yticklabels=['No', 'Sí'])
    plt.xlabel('Predicción')
    plt.ylabel('Real')
    plt.title('Matriz de Confusión')
    plt.tight_layout()
    plt.savefig(os.path.join(base_dir, 'confusion_matrix.png'))
    plt.close()

    return {
        'accuracy': acc,
        'report': classification_report(y_test, y_pred, target_names=['No', 'Sí'], output_dict=True),
        'confusion_matrix': matrix
    }

# -------------------------------------------------------
# Predicción
# -------------------------------------------------------
def predict_label(features_dict, threshold=0.5):
    input_df = pd.DataFrame([features_dict])
    input_df = input_df.replace({
        'yes': 1, 'no': 0,
        'Yes': 1, 'No': 0,
        True: 1, False: 0
    })

    # Asegurar columnas consistentes
    for col in features:  # usamos 'features' para mantener el orden exacto
        if col not in input_df.columns:
            input_df[col] = 0

    # Depuración: ver datos que entran al modelo
    print("=== Datos recibidos para predicción ===")
    print(input_df[features])

    # Escalar y predecir
    input_scaled = scaler.transform(input_df[features])
    prob = model.predict_proba(input_scaled)[0][1]

    # Depuración: ver probabilidad cruda
    print("Probabilidad cruda:", prob)

    label = 'Sí' if prob >= threshold else 'No'
    return label, prob


# -------------------------------------------------------
# Descripción del flujo
# -------------------------------------------------------
workflow_description = """
1. Carga del dataset student_dropout.csv.
2. Selección de variables relevantes (con reemplazo de una variable faltante).
3. Codificación de variables categóricas tipo sí/no.
4. División estratificada en entrenamiento (80%) y prueba (20%).
5. Escalado de variables numéricas.
6. Entrenamiento de regresión logística con regularización por defecto.
7. Evaluación del modelo: exactitud, reporte de clasificación, matriz de confusión.
8. Predicción con función personalizada y umbral ajustable.
"""

# -------------------------------------------------------
# Datos para HTML
# -------------------------------------------------------
def get_dataset_description():
    return {
        "filas": len(X_train) + len(X_test),
        "accuracy": f"{evaluate()['accuracy']:.4f}"
    }

def ensure_model():
    evaluate()

# -------------------------------------------------------
# Ejecución directa
# -------------------------------------------------------
if __name__ == '__main__':
    print(workflow_description)
    metrics = evaluate()

    ejemplo = {
        'Final_Grade': 14,
        'Number_of_Absences': 5,
        'Study_Time': 3,
        'School_Support': 'yes'
    }
    resultado, probabilidad = predict_label(ejemplo)
    print(f'\nPredicción: {resultado} (Probabilidad: {probabilidad})')
