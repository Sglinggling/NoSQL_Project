import redis
import json
import time

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def refresh_caches():
    print(f"[{time.strftime('%H:%M:%S')}] --- Mise à jour du cache (TTL 30s) ---")
    
    # 1. Cache Top 5 livreurs [cite: 187]
    top_drivers_raw = r.zrevrange("drivers:ratings", 0, 4, withscores=True)
    top_list = []
    for d_id, score in top_drivers_raw:
        nom = r.hget(f"driver:{d_id}", "nom")
        top_list.append({"id": d_id, "nom": nom, "rating": score})
    
    # Stockage avec expiration [cite: 189]
    r.setex("cache:top5_drivers", 30, json.dumps(top_list))

    # 2. Cache Commandes en attente par région [cite: 188]
    pending_ids = r.smembers("orders:status:en_attente")
    by_region = {}
    for c_id in pending_ids:
        dest = r.hget(f"order:{c_id}", "destination")
        if dest:
            if dest not in by_region: by_region[dest] = []
            by_region[dest].append(c_id)

    for region, ids in by_region.items():
        r.setex(f"cache:orders_pending:{region}", 30, json.dumps(ids))

    print("✓ Caches actualisés.")

if __name__ == "__main__":
    print("Worker de cache démarré... (Ctrl+C pour arrêter)")
    try:
        while True:
            refresh_caches()
            time.sleep(30) # Fréquence de rafraîchissement [cite: 189]
    except KeyboardInterrupt:
        print("Arrêt du worker.")