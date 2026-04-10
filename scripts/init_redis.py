import redis
import time

# Connexion à Redis
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def init_db():
    print("--- Initialisation de Redis ---")
    r.flushall()

    # Les livreurs
    drivers = {
        "d1": {"nom": "Alice Dupont", "region": "Paris", "rating": 4.8, "encours": 0, "finies": 0},
        "d2": {"nom": "Bob Martin", "region": "Paris", "rating": 4.5, "encours": 0, "finies": 0},
        "d3": {"nom": "Charlie Lefevre", "region": "Banlieue", "rating": 4.9, "encours": 0, "finies": 0},
        "d4": {"nom": "Diana Russo", "region": "Banlieue", "rating": 4.3, "encours": 0, "finies": 0},
    }

    for d_id, data in drivers.items():
        # Stockage profil complet (Hash)
        r.hset(f"driver:{d_id}", mapping=data)
        # Stockage pour classement 
        r.zadd("drivers:ratings", {d_id: data["rating"]})

    # Les commandes
    orders = {
        "c1": {"client": "Client A", "destination": "Marais", "montant": 25, "statut": "en_attente"},
        "c2": {"client": "Client B", "destination": "Belleville", "montant": 15, "statut": "en_attente"},
        "c3": {"client": "Client C", "destination": "Bercy", "montant": 30, "statut": "en_attente"},
        "c4": {"client": "Client D", "destination": "Auteuil", "montant": 20, "statut": "en_attente"},
    }

    for c_id, data in orders.items():
        data["created_at"] = int(time.time())
        # Stockage commande (Hash)
        r.hset(f"order:{c_id}", mapping=data)
        # Groupement par statut (Set) [cite: 77-78]
        r.sadd("orders:status:en_attente", c_id)

    print("Initialisation terminée : 4 livreurs et 4 commandes créés.")

if __name__ == "__main__":
    init_db()