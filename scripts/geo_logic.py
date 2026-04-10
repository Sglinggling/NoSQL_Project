import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def init_geo():
    # 1. Stocker les lieux de livraison
    r.geoadd("delivery_points", [2.364, 48.861, "Marais"])
    r.geoadd("delivery_points", [2.379, 48.870, "Belleville"])
    r.geoadd("delivery_points", [2.381, 48.840, "Bercy"])
    r.geoadd("delivery_points", [2.254, 48.851, "Auteuil"])

    # 2. Stocker les positions des livreurs
    r.geoadd("drivers_locations", [2.365, 48.862, "d1"])
    r.geoadd("drivers_locations", [2.378, 48.871, "d2"])
    r.geoadd("drivers_locations", [2.320, 48.920, "d3"])
    r.geoadd("drivers_locations", [2.400, 48.750, "d4"])
    print("Positions géo-spatiales initialisées.")

def trouver_proches():
    print("\n--- Recherche des livreurs proches du Marais ---")
    
    # 1. On récupère d'abord la position du Marais dans 'delivery_points'
    pos_marais = r.geopos("delivery_points", "Marais")
    
    if not pos_marais or not pos_marais[0]:
        print("Erreur : Le lieu 'Marais' est introuvable.")
        return

    lon, lat = pos_marais[0]
    print(f"Position du Marais : Longitude {lon}, Latitude {lat}")

    # 2. On cherche les livreurs dans 'drivers_locations' autour de ces coordonnées
    # On utilise longitude/latitude au lieu de member/member_key
    proches = r.geosearch(
        "drivers_locations",
        longitude=lon,
        latitude=lat,
        radius=2,
        unit="km",
        withdist=True,
        withcoord=True,
        sort="ASC" # Pour avoir le plus proche en premier 
    )

    if proches:
        for p in proches:
            d_id, dist, coord = p
            print(f"Livreur trouvé : {d_id} à {dist:.3f} km")
    else:
        print("Aucun livreur trouvé dans un rayon de 2 km.")

def affectation_optimale(lieu="Marais"):
    print(f"\nAffectation optimale pour le {lieu} ---")
    
    # 1. Récupérer la position du lieu
    pos = r.geopos("delivery_points", lieu)
    if not pos or not pos[0]: return
    lon, lat = pos[0]

    # 2. Trouver les livreurs dans un rayon de 3 km
    candidats = r.geosearch(
        "drivers_locations",
        longitude=lon, latitude=lat,
        radius=3, unit="km",
        withdist=True
    )

    liste_candidats = []
    for d_id, dist in candidats:
        # 3. Récupérer le rating depuis le Hash du livreur
        rating = r.hget(f"driver:{d_id}", "rating")
        rating = float(rating) if rating else 0.0
        
        liste_candidats.append({"id": d_id, "dist": dist, "rating": rating})
        print(f"Livreur {d_id} : Distance {dist:.3f} km | Note : {rating}/5")

    if liste_candidats:
        meilleur = max(liste_candidats, key=lambda x: x['rating'])
        print(f"Meilleur choix trouvé : {meilleur['id']}")
        return meilleur['id']  # <--- AJOUTE CETTE LIGNE
    return None

if __name__ == "__main__":
    init_geo()
    trouver_proches()
    affectation_optimale("Marais")
