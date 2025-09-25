# prep_german.py
import os
import numpy as np
import pandas as pd

RAW_PATH = "data/german.data"
OUT_PATH = "data/credit_demo.csv"
RNG = np.random.RandomState(42)

COLS = [
    "Status_Checking","Duration_Month","Credit_History","Purpose","Credit_Amount",
    "Savings_Status","Employment_Since","Installment_Rate","Personal_Status_Sex",
    "Other_Debtors","Residence_Since","Property","Age","Other_Installment",
    "Housing","Existing_Credits","Job","Liable_People","Telephone","Foreign_Worker","Target"
]

def load_raw(path: str) -> pd.DataFrame:
    return pd.read_csv(path, sep=" ", header=None, names=COLS)

def map_historial_crediticio(x: str) -> str:
    if x in ("A30","A31"): return "Excelente"
    if x == "A32": return "Bueno"
    if x == "A33": return "Regular"
    return "Malo"

def map_tipo_empleo(job: str, emp: str) -> str:
    if job in ("A171","A172"): return "Temporal"
    if job in ("A173","A174"): return "Dependiente"
    return "Dependiente" if emp in ("A73","A74","A75") else "Temporal"

def derive_ingresos_mensuales(sav: str, emp: str) -> int:
    base = {"A61":(1200000,2500000),"A62":(1800000,3200000),"A63":(2500000,4000000),"A64":(3500000,6000000),"A65":(1500000,3000000)}
    bonus = {"A71":0.9,"A72":0.95,"A73":1.0,"A74":1.1,"A75":1.2}
    lo, hi = base.get(sav,(1800000,3200000))
    mult = bonus.get(emp,1.0)
    return int(max(RNG.uniform(lo,hi)*mult, 900000))

def map_endeudamiento(rate: int) -> float:
    return {1:0.2, 2:0.35, 3:0.55, 4:0.75}.get(rate, 0.35)

def map_target(t: int|str) -> str:
    # UCI: 1=Good, 2=Bad
    try:
        t = int(t)
    except:
        pass
    return "Sí" if t == 1 else "No"

def main():
    if not os.path.exists(RAW_PATH):
        raise FileNotFoundError(f"No se encontró {RAW_PATH}")
    df = load_raw(RAW_PATH)
    out = pd.DataFrame({
        "historial_crediticio": df["Credit_History"].map(map_historial_crediticio),
        "nivel_endeudamiento": df["Installment_Rate"].map(map_endeudamiento).astype(float),
        "ingresos_mensuales": [derive_ingresos_mensuales(s,e) for s,e in zip(df["Savings_Status"], df["Employment_Since"])],
        "edad": df["Age"].astype(int),
        "tipo_empleo": [map_tipo_empleo(j,e) for j,e in zip(df["Job"], df["Employment_Since"])],
        "aprobacion": df["Target"].map(map_target)
    })
    assert out.isnull().sum().sum() == 0
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    out.to_csv(OUT_PATH, index=False, encoding="utf-8")
    print(f"Guardado {OUT_PATH}; filas: {len(out)}")

if __name__ == "__main__":
    main()
