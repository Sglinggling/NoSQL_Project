import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def afficher_tout():
    print("DASHBOARD TEMPS RÉEL")

    # --- LIVREURS (Travail n°1 & 6) ---
    print("\n[LIVREURS ACTIFS]")
    # On récupère le classement via le Sorted Set [cite: 70-71]
    top_drivers = r.zrevrange("drivers:ratings", 0, -1, withscores=True)
    for d_id, rating in top_drivers:
        # On récupère le reste des infos dans le Hash [cite: 68]
        info = r.hgetall(f"driver:{d_id}")
        print(f"ID: {d_id} | {info['nom']} | Région: {info['region']} | {rating}/5 | En cours: {info.get('encours', 0)}")

    # --- COMMANDES (Travail n°4 & 6) --- [cite: 87, 98]
    for statut in ["en_attente", "assignee", "livree"]:
        ids = r.smembers(f"orders:status:{statut}")
        print(f"\n[COMMANDES {statut.upper()}] ({len(ids)} commande(s))")
        for c_id in ids:
            details = r.hgetall(f"order:{c_id}") # Récupère les détails du prof [cite: 75-76]
            print(f"  - {c_id}: {details['client']} -> {details['destination']} ({details['montant']}€)")

    # --- MEILLEUR LIVREUR (Travail n°4) --- [cite: 90]
    best = r.zrevrange("drivers:ratings", 0, 0, withscores=True)
    if best:
        d_id, score = best[0]
        nom = r.hget(f"driver:{d_id}", "nom")
        print(f"\n Meilleur livreur actuel : {nom} ({score}/5)")

if __name__ == "__main__":
    afficher_tout()