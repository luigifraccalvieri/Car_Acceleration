from math import sqrt
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OrdinalEncoder
from sklearn.feature_selection import f_classif
import matplotlib.pyplot as plt

# Fonte: https://jtemporal.com/kmeans-and-elbow-method/#:~:text=import%20seaborn%20as%20sns%20from%20sklearn.cluster%20import%20KMeans,of%20clusters%20kmeans%20%3D%20KMeans%28n_clusters%3Dn%29%20clusters%20%3D%20kmeans.fit_predict%28df%29
def optimal_number_of_clusters(sse, range_bottom, range_top):
    x1, y1 = range_bottom, sse[0]
    x2, y2 = range_top, sse[len(sse)-1]

    distances = []
    for i in range(len(sse)):
        x0 = i+2
        y0 = sse[i]
        numerator = abs((y2-y1)*x0 - (x2-x1)*y0 + x2*y1 - y2*x1)
        denominator = sqrt((y2 - y1)**2 + (x2 - x1)**2)
        distances.append(numerator/denominator)
        
    return distances.index(max(distances)) + 2

# Caricamento del dataset
data = pd.read_csv('datasets/preprocessed.csv', dtype=str)

data2 = data.copy()

# Selezione delle caratteristiche da utilizzare per la clusterizzazione
features = ['make', 'model', 'generation', 'year_from', 'year_to', 'series', 'length_mm', 'width_mm', 'height_mm', 'wheelbase_mm', 'front_track_mm', 'rear_track_mm', 'curb_weight_kg', 'max_trunk_capacity_l', 'minimum_trunk_capacity_l', 'maximum_torque_n_m', 'injection_type', 'cylinder_layout', 'number_of_cylinders', 'engine_type', 'valves_per_cylinder', 'boost_type', 'cylinder_bore_mm', 'stroke_cycle_mm', 'turnover_of_maximum_torque_rpm', 'capacity_cm3', 'engine_hp', 'engine_hp_rpm', 'drive_wheels', 'number_of_gears', 'transmission', 'fuel_tank_capacity_l', 'max_speed_km_per_h', 'city_fuel_per_100km_l','acceleration_0_100_km/h_s', 'fuel_grade', 'highway_fuel_per_100km_l', 'back_suspension', 'front_suspension']

# Trasformazione dei dati discreti in continui
categorical_features = ['make', 'model', 'generation', 'series', 'injection_type', 'cylinder_layout', 'engine_type', 'boost_type', 'drive_wheels', 'transmission', 'fuel_grade', 'back_suspension', 'front_suspension']
encoder = OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1)
data[categorical_features] = encoder.fit_transform(data[categorical_features])

# Preprocessing dei dati
X = data[features].values

# Normalizzazione dei dati
scaler = StandardScaler()
X = scaler.fit_transform(X)

# Numero minimo e massimo di clusters da testare
range_bottom = 2
range_top = 25

# Definizione del range di valori di k da testare
k_range = range(range_bottom, range_top+1)

# Calcolo della somma dei quadrati delle distanze per ogni valore di k
sse = []
for k in k_range: # per costruzione python non cicla su k 41
    kmeans = KMeans(n_clusters=k, random_state=0, n_init=10)
    kmeans.fit(X)
    sse.append(kmeans.inertia_)

# Stampa della curva del gomito
plt.plot(k_range, sse, 'bx-')
plt.xlabel('Numero di cluster (k)')
plt.ylabel('Somma dei quadrati delle distanze')
plt.title('Curva del gomito')
plt.show()

best_k = optimal_number_of_clusters(sse, range_bottom, range_top)
print("Numero ottimale di cluster:", best_k)

# Esecuzione del clustering con il numero ottimale di cluster
kmeans = KMeans(n_clusters=best_k, random_state=0, n_init=10)
kmeans.fit(X)

# Aggiunta delle etichette di cluster al dataset
data['cluster'] = kmeans.labels_

# Modifica delle etichette di cluster
data['cluster'] = data['cluster'].apply(lambda x: x + 1)

#data[features] = data2[features]
data2['cluster'] = data['cluster']

# Salvataggio del dataset modificato in un file csv
data2.to_csv('datasets/clustered.csv', index=False)
