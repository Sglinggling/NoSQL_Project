import redis
import json

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def afficher_tout():
    # --- TA PREMIÈRE PARTIE ---
    print("DASHBOARD TEMPS RÉEL")

    # --- LIVREURS (Travail n°1 & 6) ---
    print("\n[LIVREURS ACTIFS]")
    # On récupère le classement via le Sorted Set 
    top_drivers = r.zrevrange("drivers:ratings", 0, -1, withscores=True)
    for d_id, rating in top_drivers:
        # On récupère le reste des infos dans le Hash
        info = r.hgetall(f"driver:{d_id}")
        print(f"ID: {d_id} | {info['nom']} | Région: {info['region']} | {rating}/5 | En cours: {info.get('encours', 0)}")

    # --- COMMANDES (Travail n°4 & 6) --- 
    for statut in ["en_attente", "assignee", "livree"]:
        ids = r.smembers(f"orders:status:{statut}")
        print(f"\n[COMMANDES {statut.upper()}] ({len(ids)} commande(s))")
        for c_id in ids:
            details = r.hgetall(f"order:{c_id}") 
            print(f"  - {c_id}: {details['client']} -> {details['destination']} ({details['montant']}€)")

    # --- MEILLEUR LIVREUR (Travail n°4) --- 
    best = r.zrevrange("drivers:ratings", 0, 0, withscores=True)
    if best:
        d_id, score = best[0]
        nom = r.hget(f"driver:{d_id}", "nom")
        print(f"\n Meilleur livreur actuel : {nom} ({score}/5)")

    # --- LA SUITE AJUSTÉE POUR LE CACHE (Partie 3) ---
    print("\n" + "="*40)
    print("[VUE DES CACHES - OPTIMISATION (TTL 30s)]")
    print("="*40)
    
    # 1. Top 5 livreurs par rating 
    cache_top5 = r.get("cache:top5_drivers")
    print("\n🏆 TOP 5 LIVREURS (CACHE) :")
    if cache_top5:
        top5_data = json.loads(cache_top5)
        for i, driver in enumerate(top5_data, 1):
            print(f"  {i}. {driver['nom']} ({driver['rating']}/5)")
    else:
        print("  ⚠️ Cache expiré ou non généré (lancez gestion_cache.py)")

    # 2. Commandes en attente par région 
    print("\n COMMANDES EN ATTENTE PAR RÉGION (CACHE) :")
    # On vérifie les régions principales définies dans le projet
    regions = ["Marais", "Belleville", "Bercy", "Auteuil"]
    found_cache = False
    
    for reg in regions:
        cache_reg = r.get(f"cache:orders_pending:{reg}")
        if cache_reg:
            found_cache = True
            cmd_ids = json.loads(cache_reg)
            print(f"  - {reg} : {len(cmd_ids)} commande(s) {cmd_ids}")
    
    if not found_cache:
        print("  Aucun cache régional disponible (TTL 30s) [cite: 189]")

if __name__ == "__main__":
    afficher_tout()