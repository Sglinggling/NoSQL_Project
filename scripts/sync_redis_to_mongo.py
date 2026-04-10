import redis
from pymongo import MongoClient
from datetime import datetime
import sys

# Connexion globale Redis
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def cloturer_et_synchroniser(commande_id, livreur_id, avis_client, note_client):
    """
    Simule la fin d'une livraison dans Redis et transfère les données 
    vers l'historique MongoDB.
    """
    
    # 1. Connexions aux services
    try:
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
        "duration_minutes": 20, # On peut simuler une durée
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

        # 5. Mise à jour de Redis (ATOMICITÉ VIA PIPELINE)
        pipe = r.pipeline()
        
        # Changement du statut dans le Hash
        pipe.hset(f"order:{commande_id}", "statut", "livree")
        
        # --- CORRECTION : DÉPLACEMENT ENTRE LES SETS ---
        pipe.srem("orders:status:assignee", commande_id)
        pipe.sadd("orders:status:livree", commande_id)
        # -----------------------------------------------

        # Mise à jour des compteurs du livreur
        pipe.hincrby(f"driver:{livreur_id}", "encours", -1) 
        pipe.hincrby(f"driver:{livreur_id}", "finies", 1)
        
        pipe.execute()
        print(f"État Redis mis à jour : {livreur_id} est libre et {commande_id} est marquée livrée.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/sync_redis_to_mongo.py <order_id>")
    else:
        c_id = sys.argv[1]
        # On va chercher QUI était le livreur assigné
        d_id = r.get(f"assignment:{c_id}")
        
        if d_id:
            cloturer_et_synchroniser(
                commande_id=c_id, 
                livreur_id=d_id, 
                avis_client="Livraison impeccable, chauffeur très pro !", 
                note_client=5.0
            )
        else:
            print(f"Erreur : La commande {c_id} n'est assignée à personne dans Redis.")