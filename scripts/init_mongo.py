from pymongo import MongoClient

def init_mongodb():
    # Connexion à l'instance MongoDB locale définie dans le docker-compose
    client = MongoClient("mongodb://localhost:27017/")
    
    # Création (ou sélection) de la base de données du projet
    db = client["projet_livraison"]
    
    # ==========================================
    # 1. INITIALISATION DES LIVREURS
    # ==========================================

    collection_livreurs = db["livreurs"]
    collection_livreurs.drop() # Vider la collection
    
    livreurs = [
        {"_id": "d1", "nom": "Alice Dupont", "region": "Paris", "rating": 4.8},
        {"_id": "d2", "nom": "Bob Martin", "region": "Paris", "rating": 4.5},
        {"_id": "d3", "nom": "Charlie Lefevre", "region": "Banlieue", "rating": 4.9},
        {"_id": "d4", "nom": "Diana Russo", "region": "Banlieue", "rating": 4.3}
    ]
    
    resultat_livreurs = collection_livreurs.insert_many(livreurs)
    print(f"Succès ! {len(resultat_livreurs.inserted_ids)} livreurs ont été insérés dans MongoDB.")
    
    # ==========================================
    # 2. INITIALISATION DES COMMANDES
    # ==========================================
    collection_commandes = db["commandes"]
    collection_commandes.drop() # Vider la collection
    
    commandes = [
        {"_id": "c1", "client": "Client A", "destination": "Marais", "montant": 25, "creee_a": "14:00"},
        {"_id": "c2", "client": "Client B", "destination": "Belleville", "montant": 15, "creee_a": "14:05"},
        {"_id": "c3", "client": "Client C", "destination": "Bercy", "montant": 30, "creee_a": "14:10"},
        {"_id": "c4", "client": "Client D", "destination": "Auteuil", "montant": 20, "creee_a": "14:15"}
    ]
    
    resultat_commandes = collection_commandes.insert_many(commandes)
    print(f"Succès ! {len(resultat_commandes.inserted_ids)} commandes ont été insérées dans MongoDB.")

if __name__ == "__main__":
    init_mongodb()