from pymongo import MongoClient

def execute_analyses():
    # Connexion à MongoDB
    client = MongoClient("mongodb://localhost:27017/")
    db = client["projet_livraison"]
    # Harmonisation sur la collection "historique_livraison" pour que les requêtes fonctionnent
    collection = db["historique_livraison"]

    print("=== HISTORIQUE DU LIVREUR D1 ===")
    
    # 1. Afficher toutes les livraisons du livreur d1 
    print("\nListe des livraisons pour d1 :")
    livraisons_d1 = collection.find({"driver_id": "d1"})
    for doc in livraisons_d1:
        print(doc)

    # 2. Nombre et montant total pour d1 
    pipeline_d1 = [
        {"$match": {"driver_id": "d1"}},
        {
            "$group": {
                "_id": "$driver_id",
                "nombre_livraisons": {"$sum": 1},
                "montant_total": {"$sum": "$amount"}
            }
        }
    ]
    stats_d1 = list(collection.aggregate(pipeline_d1))
    if stats_d1:
        print(f"\nStats d1 -> Nombre: {stats_d1[0]['nombre_livraisons']}, Total: {stats_d1[0]['montant_total']}€")

    print("\n" + "="*50 + "\n")

    print("=== PERFORMANCE PAR RÉGION ===")
    
    # Agrégation par région avec calculs et tri 
    pipeline_regions = [
        {
            "$group": {
                "_id": "$region",
                "nombre_livraisons": {"$sum": 1}, 
                "revenu_total": {"$sum": "$amount"}, # Ajout de la virgule manquante
                "duree_moyenne": {"$avg": "$duration_minutes"},
                "rating_moyen": {"$avg": "$rating"}
            }
        },
        {
            "$sort": {"revenu_total": -1}
        }
    ]
    
    stats_regions = collection.aggregate(pipeline_regions)
    
    for reg in stats_regions:
        print(f"Région: {reg['_id']}")
        print(f" - Livraisons: {reg['nombre_livraisons']}")
        print(f" - Revenu Total: {reg['revenu_total']}€")
        print(f" - Durée moyenne: {round(reg['duree_moyenne'], 2)} min")
        print(f" - Rating moyen: {round(reg['rating_moyen'], 2)}/5")
        print("-" * 20)


    print("=== TOP 2 DES LIVREURS ===")

    pipeline_top = [
        {
            "$group": {
                "_id": "$driver_id",
                # On récupère le nom (on prend le premier rencontré)
                "driver_name": {"$first": "$driver_name"}, 
                "nb_livraisons": {"$sum": 1},
                "revenu_total": {"$sum": "$amount"},
                "duree_moyenne": {"$avg": "$duration_minutes"},
                "rating_moyen": {"$avg": "$rating"}
            }
        },
        {
            "$sort": {"revenu_total": -1} # Tri par revenu décroissant 
        },
        {
            "$limit": 2 # Retourne uniquement le top 2 
        }
    ]

    resultats = collection.aggregate(pipeline_top)

    for i, res in enumerate(resultats, 1):
        print(f"Top {i}: {res['_id']} (Revenu: {res['revenu_total']}€)")
        print(f"   - Livraisons: {res['nb_livraisons']}")
        print(f"   - Moyennes: {round(res['duree_moyenne'], 1)} min | {round(res['rating_moyen'], 1)}/5")

def appliquer_index():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["projet_livraison"]
    collection = db["deliveries"]

    # 1. Index simple sur driver_id 
    collection.create_index([("driver_id", 1)])
    print("Index sur 'driver_id' créé.")

    # 2. Index composé sur region et delivery_time 
    collection.create_index([("region", 1), ("delivery_time", 1)])
    print("Index composé sur 'region' + 'delivery_time' créé.")

if __name__ == "__main__":
    execute_analyses()
    appliquer_index()