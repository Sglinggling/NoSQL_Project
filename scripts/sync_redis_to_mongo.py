import redis
from pymongo import MongoClient
from datetime import datetime

def cloturer_et_synchroniser(commande_id, livreur_id, avis_client, note_client):
    """
    Simule la fin d'une livraison dans Redis et transfère les données 
    vers l'historique MongoDB.
    """
    
    # 1. Connexions aux services
    try:
        r = redis.Redis(host='localhost', port=6379, decode_responses=True)
        mongo_client = MongoClient("mongodb://localhost:27017/")
        db_mongo = mongo_client["projet_livraison"]
        collection_deliveries = db_mongo["historique_livraison"]
    except Exception as e:
        print(f"Erreur de connexion : {e}")
        return

    # 2. Récupération des données 
    commande_data = r.hgetall(f"order:{commande_id}") 
    livreur_data = r.hgetall(f"driver:{livreur_id}")

    if not commande_data or not livreur_data:
        print(f"Erreur : Données introuvables pour {commande_id} ou {livreur_id}")
        return

    # 3. Préparation du document pour MongoDB
    historique_doc = {
        "command_id": commande_id,
        "client": commande_data.get("client"),
        "driver_id": livreur_id,
        "driver_name": livreur_data.get("nom"),
        "delivery_time": datetime.now(), 
        "duration_minutes": 20, 
        "amount": float(commande_data.get("montant", 0)),
        "region": livreur_data.get("region"),
        "rating": float(note_client),
        "review": avis_client,
        "status": "completed"
    }

    # 4. Insertion dans MongoDB
    result = collection_deliveries.insert_one(historique_doc)
    if result.inserted_id:
        print(f"✓ Synchronisation réussie : Livraison {commande_id} archivée dans MongoDB.")

        # 5. Mise à jour de Redis (CORRECTION DES PRÉFIXES ET DES NOMS DE CHAMPS)
        r.hset(f"order:{commande_id}", "statut", "livree")
        # Ton init_redis utilise 'encours' et 'finies' comme noms de champs
        r.hincrby(f"driver:{livreur_id}", "encours", -1) 
        r.hincrby(f"driver:{livreur_id}", "finies", 1)
        
        print(f"✓ État Redis mis à jour : {livreur_id} a terminé sa course.")

if __name__ == "__main__":
    cloturer_et_synchroniser(
        commande_id="c1", 
        livreur_id="d3", 
        avis_client="Excellent service, très rapide !", 
        note_client=4.9
    )