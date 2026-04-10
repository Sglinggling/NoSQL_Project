import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def display_dashboard():
    print("\n=== DASHBOARD TEMPS RÉEL ===")
    
    # 1. Commandes par statut [cite: 98]
    attente = r.scard("orders:status:en_attente")
    assignees = r.scard("orders:status:assignee")
    livrees = r.scard("orders:status:livree")
    print(f"Commandes : {attente} en attente, {assignees} assignées, {livrees} livrées")
    
    # 2. Livraisons par livreur [cite: 99]
    print("\nCharge des livreurs :")
    for d_id in ["d1", "d2", "d3", "d4"]:
        nom = r.hget(f"driver:{d_id}", "nom")
        encours = r.hget(f"driver:{d_id}", "encours")
        print(f"- {nom} ({d_id}) : {encours} livraison(s) en cours")

    # 3. Top 2 livreurs [cite: 100]
    top = r.zrevrange("drivers:ratings", 0, 1, withscores=True)
    print("\nTop 2 Meilleurs Livreurs :")
    for d_id, score in top:
        nom = r.hget(f"driver:{d_id}", "nom")
        print(f"- {nom} : {score}/5")

if __name__ == "__main__":
    display_dashboard()