import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.preprocessing import StandardScaler


data = pd.read_csv('data.csv')

print(data.head())
print(data.info())
print(data.describe())

x = data.drop('BloodPressure', axis=1)
y = data['BloodPressure']

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)
Logistic_model = LogisticRegression()
Logistic_model.fit(x_train, y_train)             

y_pred = Logistic_model.predict(x_test)
conf_matrix = confusion_matrix(y_test, y_pred)

plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', cbar= False)
plt.xlabel('Predictet')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.show()

print(classification_report(y_test, y_pred))

accuaracy = accuracy_score(y_test, y_pred)
print(f'Exactitud del modelo:  {accuaracy *100:.2f}%')