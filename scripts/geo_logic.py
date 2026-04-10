import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def init_geo():
    # 1. Stocker les lieux de livraison [cite: 199, 205]
    r.geoadd("delivery_points", [2.364, 48.861, "Marais"])
    r.geoadd("delivery_points", [2.379, 48.870, "Belleville"])
    r.geoadd("delivery_points", [2.381, 48.840, "Bercy"])
    r.geoadd("delivery_points", [2.254, 48.851, "Auteuil"])

    # 2. Stocker les positions des livreurs [cite: 202, 206]
    r.geoadd("drivers_locations", [2.365, 48.862, "d1"])
    r.geoadd("drivers_locations", [2.378, 48.871, "d2"])
    r.geoadd("drivers_locations", [2.320, 48.920, "d3"])
    r.geoadd("drivers_locations", [2.400, 48.750, "d4"])
    print("Positions géo-spatiales initialisées.")

def trouver_proches():
    # Trouver livreurs à moins de 2km du Marais [cite: 211-212]
    proches = r.geosearch(
        "drivers_locations",
        member="Marais",
        member_key="delivery_points",
        radius=2,
        unit="km",
        withdist=True
    )
    print(f"\nLivreurs à moins de 2km du Marais : {proches}")

if __name__ == "__main__":
    init_geo()
    trouver_proches()