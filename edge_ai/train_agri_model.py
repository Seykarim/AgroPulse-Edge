import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

def generate_agri_dataset(samples=2500):
    np.random.seed(42)
    
    soil_moisture = np.random.uniform(10, 70, samples)     # %
    soil_temp = np.random.uniform(18, 35, samples)         # °C
    air_temp = np.random.uniform(15, 42, samples)          # °C
    air_humidity = np.random.uniform(30, 98, samples)      # %
    uv_index = np.random.uniform(1, 12, samples)           # UV
    nitrogen_ppm = np.random.uniform(5, 60, samples)       # ppm
    
    # Target: 0: Normal, 1: Necesidad Riego, 2: Riesgo Hongo/Plaga, 3: Alerta Estrés Térmico
    status = []
    for i in range(samples):
        if air_humidity[i] > 85 and 18 <= air_temp[i] <= 26:
            status.append(2) # Riesgo de hongo (Roya/Sigatoka/Monilia)
        elif soil_moisture[i] < 22 and uv_index[i] > 7:
            status.append(3) # Estrés térmico/hídrico crítico
        elif soil_moisture[i] < 30:
            status.append(1) # Necesidad de Riego
        else:
            status.append(0) # Estado Saludable
            
    df = pd.DataFrame({
        'soil_moisture': soil_moisture, 'soil_temp': soil_temp,
        'air_temp': air_temp, 'air_humidity': air_humidity,
        'uv_index': uv_index, 'nitrogen_ppm': nitrogen_ppm,
        'status': status
    })
    return df

def main():
    print("🌾 AgroPulse Edge AI - Entrenando Clasificador de Riesgo Agropecuario...")
    df = generate_agri_dataset()
    
    X = df.drop('status', axis=1)
    y = df['status']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    clf = RandomForestClassifier(n_estimators=12, max_depth=6, random_state=42)
    clf.fit(X_train, y_train)
    
    acc = clf.score(X_test, y_test)
    print(f"✅ Exactitud del Modelo Evaluado: {acc * 100:.2f}%\n")
    print(classification_report(y_test, clf.predict(X_test)))

    with open("edge_ai/model_summary.txt", "w") as f:
        f.write(f"AgroPulse Edge AI Model\nAccuracy: {acc*100:.2f}%\nTarget Crops: Cafe, Cacao, Platano, Pastos\n")
    print("💾 Resumen del modelo guardado en edge_ai/model_summary.txt")

if __name__ == "__main__":
    main()
