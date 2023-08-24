import pandas as pd
from sklearn.ensemble import AdaBoostRegressor
from sklearn.preprocessing import OrdinalEncoder
from sklearn.model_selection import GridSearchCV

# Carica il dataset
while True:
    file = input(
        "Seleziona un file tra preprocessed(1), clustered_plus_prolog_generated(2), prolog_generated(3) e clustered(4) o 'q' per uscire: "
    )

    match file:
        case "1":
            nome_dataset = "preprocessed.csv"
            break
        case "2":
            nome_dataset = "clustered_plus_prolog_generated.csv"
            break
        case "3":
            nome_dataset = "prolog_generated.csv"
            break
        case "4":
            nome_dataset = "clustered.csv"
            break
        case "q":
            exit()
        case _:
            print("Input non valido")

data = pd.read_csv(f"datasets/{nome_dataset}")

match nome_dataset:
    case "preprocessed.csv":
        features = [
            "make",
            "model",
            "generation",
            "year_from",
            "year_to",
            "series",
            "length_mm",
            "width_mm",
            "height_mm",
            "wheelbase_mm",
            "front_track_mm",
            "rear_track_mm",
            "curb_weight_kg",
            "max_trunk_capacity_l",
            "minimum_trunk_capacity_l",
            "maximum_torque_n_m",
            "injection_type",
            "cylinder_layout",
            "number_of_cylinders",
            "engine_type",
            "valves_per_cylinder",
            "boost_type",
            "cylinder_bore_mm",
            "stroke_cycle_mm",
            "turnover_of_maximum_torque_rpm",
            "capacity_cm3",
            "engine_hp",
            "engine_hp_rpm",
            "drive_wheels",
            "number_of_gears",
            "transmission",
            "fuel_tank_capacity_l",
            "max_speed_km_per_h",
            "city_fuel_per_100km_l",
            "fuel_grade",
            "highway_fuel_per_100km_l",
            "back_suspension",
            "front_suspension",
        ]
        categorical_features = [
            "make",
            "model",
            "generation",
            "series",
            "injection_type",
            "cylinder_layout",
            "engine_type",
            "boost_type",
            "drive_wheels",
            "transmission",
            "fuel_grade",
            "back_suspension",
            "front_suspension",
        ]
    case "clustered.csv":
        features = [
            "make",
            "model",
            "generation",
            "year_from",
            "year_to",
            "series",
            "length_mm",
            "width_mm",
            "height_mm",
            "wheelbase_mm",
            "front_track_mm",
            "rear_track_mm",
            "curb_weight_kg",
            "max_trunk_capacity_l",
            "minimum_trunk_capacity_l",
            "maximum_torque_n_m",
            "injection_type",
            "cylinder_layout",
            "number_of_cylinders",
            "engine_type",
            "valves_per_cylinder",
            "boost_type",
            "cylinder_bore_mm",
            "stroke_cycle_mm",
            "turnover_of_maximum_torque_rpm",
            "capacity_cm3",
            "engine_hp",
            "engine_hp_rpm",
            "drive_wheels",
            "number_of_gears",
            "transmission",
            "fuel_tank_capacity_l",
            "max_speed_km_per_h",
            "city_fuel_per_100km_l",
            "fuel_grade",
            "highway_fuel_per_100km_l",
            "back_suspension",
            "front_suspension",
            "cluster",
        ]
        categorical_features = [
            "make",
            "model",
            "generation",
            "series",
            "injection_type",
            "cylinder_layout",
            "engine_type",
            "boost_type",
            "drive_wheels",
            "transmission",
            "fuel_grade",
            "back_suspension",
            "front_suspension",
        ]
    case "prolog_generated.csv":
        features = [
            "weight_to_power_ratio",
            "drag_coefficient",
            "specific_power",
            "length_ratio",
            "number_cylinder_capacity_ratio",
            "length_power_ratio",
            "max_speed_power_ratio",
            "power",
            "shape",
            "avg_trunk_capacity_brand",
            "most_powerful_car_brand",
            "most_common_cylinder_layout_yeargroup_of_three",
        ]
        categorical_features = [
            "power",
            "shape",
            "most_powerful_car_brand",
            "most_common_cylinder_layout_yeargroup_of_three",
        ]
    case "clustered_plus_prolog_generated.csv":
        features = [
            "make",
            "model",
            "generation",
            "year_from",
            "year_to",
            "series",
            "length_mm",
            "width_mm",
            "height_mm",
            "wheelbase_mm",
            "front_track_mm",
            "rear_track_mm",
            "curb_weight_kg",
            "max_trunk_capacity_l",
            "minimum_trunk_capacity_l",
            "maximum_torque_n_m",
            "injection_type",
            "cylinder_layout",
            "number_of_cylinders",
            "engine_type",
            "valves_per_cylinder",
            "boost_type",
            "cylinder_bore_mm",
            "stroke_cycle_mm",
            "turnover_of_maximum_torque_rpm",
            "capacity_cm3",
            "engine_hp",
            "engine_hp_rpm",
            "drive_wheels",
            "number_of_gears",
            "transmission",
            "fuel_tank_capacity_l",
            "max_speed_km_per_h",
            "city_fuel_per_100km_l",
            "fuel_grade",
            "highway_fuel_per_100km_l",
            "back_suspension",
            "front_suspension",
            "cluster",
            "weight_to_power_ratio",
            "drag_coefficient",
            "specific_power",
            "length_ratio",
            "number_cylinder_capacity_ratio",
            "length_power_ratio",
            "max_speed_power_ratio",
            "power",
            "shape",
            "avg_trunk_capacity_brand",
            "most_powerful_car_brand",
            "most_common_cylinder_layout_yeargroup_of_three",
        ]
        categorical_features = [
            "make",
            "model",
            "generation",
            "series",
            "injection_type",
            "cylinder_layout",
            "engine_type",
            "boost_type",
            "drive_wheels",
            "transmission",
            "fuel_grade",
            "back_suspension",
            "front_suspension",
            "power",
            "shape",
            "most_powerful_car_brand",
            "most_common_cylinder_layout_yeargroup_of_three",
        ]

target = "acceleration_0_100_km/h_s"

# Codifica le colonne categoriche utilizzando OrdinalEncoder per convertire le stringhe in numeri
encoder = OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1)
data[categorical_features] = encoder.fit_transform(data[categorical_features])

# Crea l'oggetto DecisionTreeRegressor
regressor = AdaBoostRegressor()

# Definisci la griglia dei parametri da testare
param_grid = {
    "n_estimators": [10, 20, 30],
    "random_state": [0],
    "learning_rate": [0.1, 0.01, 0.001]
}

# Cerca la migliore combinazione di parametri utilizzando GridSearchCV
grid_search = GridSearchCV(
    regressor,
    param_grid=param_grid,
    cv=10,
    scoring=["neg_mean_absolute_error", "neg_mean_squared_error", "max_error"],
    refit="neg_mean_squared_error",
)
grid_search.fit(data[features], data[target])

# Stampa i risultati della ricerca
print("Migliori parametri:", grid_search.best_params_)
print("Migliore score:", grid_search.best_score_)

# Stampa i punteggi di tutte le metriche
print("Risultati della ricerca a griglia:")
results = grid_search.cv_results_
pd.DataFrame(results).to_csv(f"risultati/risultati_adaboost_{nome_dataset}")
for metric in [
    "mean_test_neg_mean_absolute_error",
    "mean_test_neg_mean_squared_error",
    "mean_test_max_error",
]:
    print(f"{metric}: {results[metric]}")

best_regressor = grid_search.best_estimator_
importances = best_regressor.feature_importances_
feature_importance = pd.DataFrame({"feature": features, "importance": importances})
feature_importance = feature_importance.sort_values("importance", ascending=False)
print("Importanza delle feature:")
for index, row in feature_importance.iterrows():
    print(row["feature"], ":", row["importance"])
