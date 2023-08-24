import pandas as pd
import matplotlib.pyplot as plt

# Carica i dati dal primo file CSV
df1 = pd.read_csv("risultati/risultati_adaboost_prolog_generated.csv")

# Seleziona il valore della colonna mean_test_neg_mean_squared_error con rank_test_neg_mean_squared_error uguale a 1 e lo converte in valore positivo
y1 = abs(df1.loc[df1['rank_test_neg_mean_squared_error'] == 1, 'mean_test_neg_mean_squared_error'].values[0])

# Seleziona il valore della colonna params con rank_test_neg_mean_squared_error uguale a 1
x1 = df1.loc[df1['rank_test_neg_mean_squared_error'] == 1, 'params'].values[0]

# Carica i dati dal secondo file CSV
df2 = pd.read_csv("risultati/risultati_decision_tree_prolog_generated.csv")

# Seleziona il valore della colonna mean_test_neg_mean_squared_error con rank_test_neg_mean_squared_error uguale a 1 e lo converte in valore positivo
y2 = abs(df2.loc[df2['rank_test_neg_mean_squared_error'] == 1, 'mean_test_neg_mean_squared_error'].values[0])

# Seleziona il valore della colonna params con rank_test_neg_mean_squared_error uguale a 1
x2 = df2.loc[df2['rank_test_neg_mean_squared_error'] == 1, 'params'].values[0]

# Carica i dati dal terzo file CSV
df3 = pd.read_csv("risultati/risultati_knn_prolog_generated.csv")

# Seleziona il valore della colonna mean_test_neg_mean_squared_error con rank_test_neg_mean_squared_error uguale a 1 e lo converte in valore positivo
y3 = abs(df3.loc[df3['rank_test_neg_mean_squared_error'] == 1, 'mean_test_neg_mean_squared_error'].values[0])

# Seleziona il valore della colonna params con rank_test_neg_mean_squared_error uguale a 1
x3 = df3.loc[df3['rank_test_neg_mean_squared_error'] == 1, 'params'].values[0]

# Carica i dati dal quarto file CSV
df4 = pd.read_csv("risultati/risultati_random_forest_prolog_generated.csv")

# Seleziona il valore della colonna mean_test_neg_mean_squared_error con rank_test_neg_mean_squared_error uguale a 1 e lo converte in valore positivo
y4 = abs(df4.loc[df4['rank_test_neg_mean_squared_error'] == 1, 'mean_test_neg_mean_squared_error'].values[0])

# Seleziona il valore della colonna params con rank_test_neg_mean_squared_error uguale a 1
x4 = df4.loc[df4['rank_test_neg_mean_squared_error'] == 1, 'params'].values[0]

# Crea l'istogramma
plt.bar(['AdaBoost', 'Decision Tree', 'KNN', 'Random Forest'], [y1, y2, y3, y4])
plt.xlabel("Modello")
plt.ylabel("Errore quadratico medio")
plt.title("Dataset: prolog_generated.csv")
plt.xticks(rotation=45, ha='right')

# Aggiunge i valori precisi in cima alle colonne
for i, v in enumerate([y1, y2, y3, y4]):
    plt.text(i, v + 0.01, str(round(v, 3)), ha='center', fontsize=8)

plt.show()