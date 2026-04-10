from pymongo import MongoClient

def init_mongodb():
    # Connexion à l'instance MongoDB locale définie dans le docker-compose
    client = MongoClient("mongodb://localhost:27017/")
    
    # Création (ou sélection) de la base de données du projet
    db = client["projet_livraison"]
    
    # 3. INITIALISATION DE L'HISTORIQUE (Historique livraison)
    collection_deliveries = db["historique_livraison"]
    collection_deliveries.drop()

    deliveries = [
        {
            "command_id": "c1", 
            "client": "Client A", 
            "driver_id": "d3", 
            "duration_minutes": 20, 
            "amount": 25, 
            "rating": 4.9, 
            "region": "Paris",
            "review": "Chauffeur très aimable et ponctuel !" 
        },
        {
            "command_id": "c2", 
            "client": "Client B", 
            "driver_id": "d1", 
            "duration_minutes": 15, 
            "amount": 15, 
            "rating": 4.8, 
            "region": "Paris",
            "review": "Livraison parfaite, merci." 
        },
        {
            "command_id": "c3", 
            "client": "Client C", 
            "driver_id": "d2", 
            "duration_minutes": 25, 
            "amount": 30, 
            "rating": 4.5, 
            "region": "Banlieue",
            "review": "Un peu de retard mais livreur sympa." 
        },
        {
            "command_id": "c4", 
            "client": "Client D", 
            "driver_id": "d1", 
            "duration_minutes": 18, 
            "amount": 20, 
            "rating": 4.8, 
            "region": "Paris",
            "review": "Service efficace et rapide."
        }
    ]

    collection_deliveries.insert_many(deliveries)
    print(f"Succès ! {len(deliveries)} livraisons historiques insérées dans 'historique_livraison'.")

if __name__ == "__main__":
    init_mongodb()
