import pandas as pd
from pyswip import Prolog
import pandas as pd

dataset_path = "datasets/clustered.csv"

# COSTRUISCE FACTS.PL
def load_data_in_kb():
    dataset = pd.read_csv(dataset_path, dtype=str)
    prolog_file = open("facts.pl", "w")
    
    # Consente la discontinuità sintattica delle righe nei file Prolog
    write_facts_in_file([":-style_check(-discontiguous)"], prolog_file)
    
    for index, row in dataset.iterrows():
        car_num = f"car({row['ID']})"
        facts = [f"make({car_num}, {row['make']})",
                 f"model({car_num},{row['model']})",
                 f"year_from({car_num},{row['year_from']})",
                 f"length_mm({car_num},{row['length_mm']})",
                 f"width_mm({car_num},{row['width_mm']})",
                 f"height_mm({car_num},{row['height_mm']})",
                 f"curb_weight_kg({car_num},{row['curb_weight_kg']})",
                 f"max_trunk_capacity_l({car_num},{row['max_trunk_capacity_l']})",
                 f"cylinder_layout({car_num},{row['cylinder_layout']})",
                 f"number_of_cylinders({car_num},{row['number_of_cylinders']})",
                 f"engine_type({car_num},{row['engine_type']})",
                 f"capacity_cm3({car_num},{row['capacity_cm3']})",
                 f"engine_hp({car_num},{row['engine_hp']})",
                 f"acceleration_0_100_km/h_s({car_num},{row['acceleration_0_100_km/h_s']})",
                 f"max_speed_km_per_h({car_num},{row['max_speed_km_per_h']})"]
  
        write_facts_in_file(facts, prolog_file)

    prolog_file.close()

# Con questa funzione inseriamo una lista di fatti all'interno di un file 
def write_facts_in_file(facts, kb_file):
    kb_file.writelines(".\n".join(facts) + ".\n")

# CREA LA KB
def create_kb() -> Prolog:
    prolog = Prolog()

    prolog.consult("facts.pl")

    prolog.assertz(f"weight_to_power_ratio(car(C), W) :- curb_weight_kg(car(C), K), engine_hp(car(C), H), W is K / H")

    # In questa asserzione abbiamo ipotizzato e fissato una velocità di 100kmh e una forza media di resistenza aerodinamica di 450N
    prolog.assertz(f"drag_coefficient(car(C), DragCoefficient) :- height_mm(car(C), HeightMm), width_mm(car(C), WidthMm), FrontalAreaM2 is WidthMm * HeightMm / 1000000, AirDensityKgM3 is 1.2, VelocityKmh is 100, DragCoefficient is 2 * 450 / (AirDensityKgM3 * FrontalAreaM2 * (VelocityKmh / 3.6)^2)")
   
    prolog.assertz(f"specific_power(car(C), S) :- capacity_cm3(car(C), Cap), engine_hp(car(C), H), S is H / Cap")

    prolog.assertz(f"length_ratio(car(C), L) :- length_mm(car(C), LengthMm), height_mm(car(C), HeightMm), L is LengthMm / HeightMm")
    prolog.assertz(f"number_cylinder_capacity_ratio(car(C), Cr) :- number_of_cylinders(car(C), N), capacity_cm3(car(C), Cap), Cr is N / Cap")
    prolog.assertz(f"length_power_ratio(car(C), Lpr) :- length_mm(car(C), L), engine_hp(car(C), H), Lpr is L / H")
    
    prolog.assertz(f"max_speed_power_ratio(car(C), Spr) :- max_speed_km_per_h(car(C), M), engine_hp(car(C), H), Spr is M / H")
    
    prolog.assertz(f"power(car(C), Potenza) :- engine_hp(car(C), HP), horsepower_fuzzy(HP, Potenza), !")
    
    prolog.assertz(f"horsepower_fuzzy(HP, bassa) :- HP < 150, !")
    prolog.assertz(f"horsepower_fuzzy(HP, media) :- HP >= 150, HP < 250, !")
    prolog.assertz(f"horsepower_fuzzy(HP, alta) :- HP >= 250, !")
    
    prolog.assertz(f"shape(car(C),Forma) :- height_mm(car(C), Height), width_mm(car(C), Width), forma(Forma, Height, Width), !")
    
    prolog.assertz(f"forma(sportiva, Height, Width) :- Height =< 1200, Width >= 1350, !")
    prolog.assertz(f"forma(coupé, Height, Width) :- Height > 1200, Height =< 1400, Width >= 1350, !")
    prolog.assertz(f"forma(berlina, Height, Width) :- Height >= 1400, Height < 1500, Width >= 1350, !")
    prolog.assertz(f"forma(suv, Height, Width) :- Height >= 1500, Width >= 1350, !")
 
    # Calcola la capacità media del bagagliaio delle auto di un certo brand
    prolog.assertz(f"avg_trunk_capacity(car(C), AvgCapacity) :- make(car(C), Manufacturer), " # Qui troviamo il brand della macchina in input alla regola
    "findall(Capacity, (make(car(D), Manufacturer), max_trunk_capacity_l(car(D), Capacity)), Capacities), " # Qui con findall cicliamo su tutte le macchine facenti parte dello stesso brand della macchina in input calcolando le capacità del bagagliaio di queste macchine e le mettiamo in una lista
    "sumlist(Capacities, Sum), length(Capacities, Length), Length > 0, AvgCapacity is Sum / Length")     # Qui sommiamo tutte le capacità, calcoliamo la lunghezza della lista ed infine dividiamo la somma per la lunghezza 

    # Restituisce il modello più potente di un certo brand
    prolog.assertz(f"most_powerful_car(car(C), MaxModel) :- "
        "make(car(C), Manufacturer), " # Prendo il Manufacturer dell'auto passata in input
        "findall(Power, (make(car(D), Manufacturer), engine_hp(car(D), Power)), Powers), " # Creo la lista Powers contenente i cavalli delle auto di un certo Manufacturer
        "length(Powers, NumPowers), "
        "NumPowers > 0, " # Mi assicuro la lista non sia vuota
        "max_list(Powers, MaxPower), " # Prendo il valore massimo all'interno di Powers
        "make(car(E), Manufacturer), engine_hp(car(E), MaxPower), model(car(E), MaxModel)") # Prendo i modelli delle auto di un certo Manufacturer, con un certo MaxPower

    # Restituisce l'elemento più frequente all'interno di una lista
    prolog.assertz("most_frequent_element(List, Element) :-"
                   
                   # Con findall viene creata una lista di coppie ed ogni coppia è avvalorata dal conteggio degli elementi della 
                   # sottolista in cui bagof ha raggruppato gli elementi uguali e dall'elemento preso in considerazione (Count-Elemento)
                   "  findall(Count-X, (bagof(true, member(X, List), Xs), length(Xs, Count)), Pairs),"
                   
                   # con keysort ordiniamo la lista di coppie in modo crescente (Pairs)
                   "  keysort(Pairs, SortedPairs),"
                   
                   # con reverse capovolgiamo la lista per poi estrarre con [Count-Element|_] e preleviamo solo il primo elemento della lista 
                   # (la testa Count-Element) ed ignoriamo la coda (_) 
                   "  reverse(SortedPairs, [Count-Element|_])"
                   )
    
    # Restituisce la tipologia di layout dei cilindri motore più popolare con cadenza triennale (i trienni sono fissati in modo che il primo dei tre anni sia un multiplo di tre e gli altri due no)
    # Fissato l'anno di inizio produzione dell'automobile car(C) presa in considerazione e posto in Year
    prolog.assertz(f"most_common_cylinder_layout(car(C), MostCommonCilinderLayout) :- year_from(car(C), Year), "
                    
                    "YearGroup is floor(Year / 3), " # Preso l'anno multiplo di tre per difetto relativo all'Year considerato
                    
                    # Creo una lista di elementi avvalorati dai cylinder_layout delle automobili che sono state prodotte inizialmente nello stesso triennio della car(C) presa in considerazione
                    "findall(CilinderLayout, (year_from(car(D), YearD), YearGroupD is floor(YearD / 3), YearGroup =:= YearGroupD, cylinder_layout(car(D), CilinderLayout)), CilinderLayoutList), "
                    
                    # Restituisco il cylinder_layout più frequente
                    "most_frequent_element(CilinderLayoutList, MostCommonCilinderLayout)")    

    return prolog


def produce_dataset(kb):
    dataset = pd.read_csv(dataset_path, dtype=str)

    dataset_new = pd.DataFrame()
    
    for index, row in dataset.iterrows():
        dataset_new.at[index, 'ID'] = row['ID']
        dataset_new.at[index, 'acceleration_0_100_km/h_s'] = row['acceleration_0_100_km/h_s']
        dataset_new.at[index, 'engine_type'] = row['engine_type']
        dataset_new.at[index, 'weight_to_power_ratio'] = '%.3f'%(list(kb.query(f"weight_to_power_ratio(car({row['ID']}), N)"))[0]['N'])
        dataset_new.at[index, 'drag_coefficient'] = '%.3f'%(list(kb.query(f"drag_coefficient(car({row['ID']}), N)"))[0]['N'])
        dataset_new.at[index, 'specific_power'] = '%.3f'%(list(kb.query(f"specific_power(car({row['ID']}), N)"))[0]['N'])
        dataset_new.at[index, 'length_ratio'] = '%.3f'%(list(kb.query(f"length_ratio(car({row['ID']}), N)"))[0]['N'])
        dataset_new.at[index, 'number_cylinder_capacity_ratio'] = '%.3f'%(list(kb.query(f"number_cylinder_capacity_ratio(car({row['ID']}), N)"))[0]['N'])
        dataset_new.at[index, 'length_power_ratio'] = '%.3f'%(list(kb.query(f"length_power_ratio(car({row['ID']}), N)"))[0]['N'])
        dataset_new.at[index, 'max_speed_power_ratio'] = '%.3f'%(list(kb.query(f"max_speed_power_ratio(car({row['ID']}), N)"))[0]['N'])
        dataset_new.at[index, 'power'] = (list(kb.query(f"power(car({row['ID']}), N)"))[0]['N'])
        dataset_new.at[index, 'shape'] = (list(kb.query(f"shape(car({row['ID']}), N)"))[0]['N'])
        dataset_new.at[index, 'avg_trunk_capacity_brand'] = '%.3f'%(list(kb.query(f"avg_trunk_capacity(car({row['ID']}), N)"))[0]['N'])
        dataset_new.at[index, 'most_powerful_car_brand'] = (list(kb.query(f"most_powerful_car(car({row['ID']}), N)"))[0]['N'])
        dataset_new.at[index, 'most_common_cylinder_layout_yeargroup_of_three'] = (list(kb.query(f"most_common_cylinder_layout(car({row['ID']}), N)"))[0]['N'])
        
    dataset_new.to_csv('datasets/prolog_generated.csv', index=False)
    dataset_new = dataset_new.drop(columns=['acceleration_0_100_km/h_s', 'engine_type'])
    merged_data = pd.merge(dataset, dataset_new, on='ID', how='inner')
    merged_data.to_csv('datasets/clustered_plus_prolog_generated.csv', index=False)

#MAIN
load_data_in_kb()
prolog = create_kb()
produce_dataset(prolog)