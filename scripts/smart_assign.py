import redis
from geo_logic import affectation_optimale
from redis_workflow import affecter_commande

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def auto_assign(order_id):
    # 1. On regarde où doit aller la commande
    destination = r.hget(f"order:{order_id}", "destination")
    if not destination:
        print(f"Erreur : Destination inconnue pour {order_id}")
        return

    print(f"Recherche du meilleur livreur pour {order_id} (Destination: {destination})...")

    best_driver_id = affectation_optimale(destination)

    if best_driver_id:
        affecter_commande(order_id, best_driver_id)
        print(f"Liaison réussie entre Géo et Workflow pour {order_id}")
    else:
        print("Aucun livreur n'a pu être trouvé par le module Géo.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        auto_assign(sys.argv[1])
    else:
        print("Usage: python3 scripts/smart_assign.py <order_id>")