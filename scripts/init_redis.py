import redis
import time

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def init_db():
    print("--- Initialisation de Redis ---")
    r.flushall()

    drivers = {
        "d1": {"nom": "Alice Dupont", "region": "Paris, Banlieue", "rating": 4.8, "encours": 0, "finies": 0},
        "d2": {"nom": "Bob Martin", "region": "Paris", "rating": 4.5, "encours": 0, "finies": 0},
        "d3": {"nom": "Charlie Lefevre", "region": "Banlieue", "rating": 4.9, "encours": 0, "finies": 0},
        "d4": {"nom": "Diana Russo", "region": "Banlieue", "rating": 4.3, "encours": 0, "finies": 0},
    }

    for d_id, data in drivers.items():
        r.hset(f"driver:{d_id}", mapping=data)
        r.zadd("drivers:ratings", {d_id: data["rating"]})

    # --- NOUVEAUTÉ PARTIE 3 : On AJOUTE les Sets pour la recherche multi-régions ---
    # Cette structure tourne en parallèle et sert uniquement aux nouvelles requêtes
    regions_livreurs = {
        "d1": ["Paris", "Banlieue"], 
        "d2": ["Paris"],
        "d3": ["Banlieue"],
        "d4": ["Banlieue"]
    }

    for d_id, regions in regions_livreurs.items():
        for region in regions:
            r.sadd(f"region:{region}", d_id) # Crée ex: le Set "region:Paris" avec d1 et d2

    # --- TRAVAIL 2 : LES COMMANDES ---
    orders = {
        "c1": {"client": "Client A", "destination": "Marais", "montant": 25, "statut": "en_attente"},
        "c2": {"client": "Client B", "destination": "Belleville", "montant": 15, "statut": "en_attente"},
        "c3": {"client": "Client C", "destination": "Bercy", "montant": 30, "statut": "en_attente"},
        "c4": {"client": "Client D", "destination": "Auteuil", "montant": 20, "statut": "en_attente"},
    }

    for c_id, data in orders.items():
        data["created_at"] = int(time.time())
        r.hset(f"order:{c_id}", mapping=data)
        r.sadd("orders:status:en_attente", c_id)

    print("Initialisation sécurisée terminée")

if __name__ == "__main__":
    init_db()