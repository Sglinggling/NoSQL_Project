import redis
import sys

# Connexion à Redis
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def affecter_commande(order_id, driver_id):
    """Travail n°3 : Affectation atomique [cite: 80-85]"""
    pipe = r.pipeline()
    try:
        # 1. Mise à jour statut commande
        pipe.hset(f"order:{order_id}", "statut", "assignee")
        # 2. Déplacement dans les Sets de statut 
        pipe.srem("orders:status:en_attente", order_id)
        pipe.sadd("orders:status:assignee", order_id)
        # 3. Enregistrement de l'affectation
        pipe.set(f"assignment:{order_id}", driver_id)
        # 4. Incrémenter livraisons en cours du livreur
        pipe.hincrby(f"driver:{driver_id}", "encours", 1)
        pipe.execute()
        print(f"Succès : Commande {order_id} affectée à {driver_id}")
    except Exception as e:
        print(f"Erreur lors de l'affectation : {e}")

def terminer_livraison(order_id):
    """Travail n°5 : Simulation d'une livraison terminée [cite: 91-95]"""
    driver_id = r.get(f"assignment:{order_id}")
    if not driver_id:
        print(f"Erreur : Aucun livreur trouvé pour la commande {order_id}")
        return

    pipe = r.pipeline()
    # 1. Passer le statut à 'livree'
    pipe.hset(f"order:{order_id}", "statut", "livree")
    pipe.srem("orders:status:assignee", order_id)
    pipe.sadd("orders:status:livree", order_id)
    # 2. Mise à jour des compteurs du livreur
    pipe.hincrby(f"driver:{driver_id}", "encours", -1)
    pipe.hincrby(f"driver:{driver_id}", "finies", 1)
    pipe.execute()
    print(f"Succès : Commande {order_id} marquée comme livrée par {driver_id}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 scripts/redis_workflow.py assign <order_id> <driver_id>")
        print("  python3 scripts/redis_workflow.py deliver <order_id>")
    else:
        commande = sys.argv[1]
        
        if commande == "assign" and len(sys.argv) == 4:
            # Exemple : python3 scripts/redis_workflow.py assign c1 d3
            affecter_commande(sys.argv[2], sys.argv[3])
        
        elif commande == "deliver" and len(sys.argv) == 3:
            # Exemple : python3 scripts/redis_workflow.py deliver c1
            terminer_livraison(sys.argv[2])
        
        else:
            print("Commande invalide ou arguments manquants.")