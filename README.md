# Car Acceleration
Repository associato caso di studio ICON A.A. 2022-2023. Gruppo di lavoro:
 - Giuseppe Demauro     (MAT. 738713)
 - Pier Silvio Fatiguso (MAT. 738026)
 - Luigi Fraccalvieri   (MAT. 738953)

# Installazione
Installare SWI Prolog compatibile con il proprio sistema operativo (**scaricare la versione 8**):

`https://www.swi-prolog.org/download/stable?show=all`

Posizionarsi all'interno della cartella root del progetto:

`cd Car_Acceleration`

Installare le dipendenze:

`pip install -r requirements.txt`

# Obiettivo
Il caso di studio in analisi è stato sviluppato tramite il linguaggio Python, esso ha come scopo l’effettuazione di operazioni di regressione sul tempo impiegato da un auto per accelerare da 0 a 100 km/h, per maggiori dettagli consultare la <a href="/docs/documentazione_car_acceleration.pdf">documentazione</a>.

# Organizzazione repository
* La directory `risultati` contiene i csv indicanti i risultati per tutte le combinazioni di iperparametri testati per ogni modello
* La directory `datasets` contiene il dataset originale e gli altri generati utilizzati
* La directory `generatori_grafici` contiene i file utilizzati per generare i grafici derivati dai risultati presenti nella directory relativa
* La directory `img` contiene le immagini relative ai grafici generati presenti anche all'interno della documentazione
* La directory `docs` contiene la documentazione del caso di studio
* I file `adaboost.py`, `decision_tree_learner.py`, `knn.py`, `random_forest.py` implementano i modelli di apprendimento supervisionato scelti per il caso di studio
* Il file `k_means.py` implementa il relativo modello di apprendimento non supervisionato scelto per il caso di studio
* Il file `preprocessing.py` consente l'effettuazione di operazioni di preprocessing sul dataset originale
* Il file `kb.py` genera la base di conoscenza Prolog



