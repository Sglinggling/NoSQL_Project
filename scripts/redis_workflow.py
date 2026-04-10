import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def affecter_commande(order_id, driver_id):
    """Travail n°3 : Affectation atomique via Pipeline """
    pipe = r.pipeline()
    try:
        # 1. Mise à jour statut commande
        pipe.hset(f"order:{order_id}", "statut", "assignee")
        # 2. Déplacement dans les Sets de statut
        pipe.srem("orders:status:en_attente", order_id)
        pipe.sadd("orders:status:assignee", order_id)
        # 3. Enregistrement de l'affectation
        pipe.set(f"assignment:{order_id}", driver_id)
        # 4. Incrémenter livraisons en cours du livreur [cite: 83]
        pipe.hincrby(f"driver:{driver_id}", "encours", 1)
        pipe.execute()
        print(f"Succès : Commande {order_id} affectée à {driver_id}")
    except Exception as e:
        print(f"Erreur lors de l'affectation : {e}")

def terminer_livraison(order_id):
    """Travail n°5 : Simuler la fin d'une livraison [cite: 92-95]"""
    driver_id = r.get(f"assignment:{order_id}")
    if not driver_id:
        print("Erreur : Aucun livreur assigné à cette commande.")
        return

    pipe = r.pipeline()
    # 1. Statut livrée
    pipe.hset(f"order:{order_id}", "statut", "livree")
    pipe.srem("orders:status:assignee", order_id)
    pipe.sadd("orders:status:livree", order_id)
    # 2. Mise à jour compteurs livreur
    pipe.hincrby(f"driver:{driver_id}", "encours", -1)
    pipe.hincrby(f"driver:{driver_id}", "finies", 1)
    pipe.execute()
    print(f"Succès : Livraison de {order_id} terminée par {driver_id}")

if __name__ == "__main__":
    # Test Travail n°3
    affecter_commande("c1", "d3")
    # Test Travail n°5
    # terminer_livraison("c1") # À décommenter pour tester la fin