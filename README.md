# Projet NoSQL Livraison

Système de gestion de livraisons en temps réel combinant **Redis** (temps réel) et **MongoDB** (historique et analyses), avec géolocalisation et optimisation par cache.

---

## Prérequis

- Docker & Docker Compose
- Python 3.x
- pip

---

## Démarrage

### 1. Lancer les services

```bash
docker compose up -d
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

---

## Scénario complet

Suivre ces étapes dans l'ordre pour tester l'ensemble du projet.

### Étape 1 — Initialisation

```bash
python3 scripts/init_redis.py
python3 scripts/init_mongo.py
python3 scripts/geo_logic.py
```

### Étape 2 — Lancer le cache

> Ce script doit rester actif dans un **terminal séparé**. Il se rafraîchit toutes les **30 secondes**.

```bash
python3 scripts/gestion_cache.py
```

### Étape 3 — Simuler une livraison

```bash
python3 scripts/smart_assign.py c1
python3 scripts/sync_redis_to_mongo.py c1
```

### Étape 4 — Visualiser le tableau de bord

```bash
python3 scripts/dashboard.py
```

---

## Autres scénarios d'exécution

### Redis — Gestion temps réel

```bash
python3 scripts/init_redis.py
python3 scripts/redis_workflow.py assign c1 d3
python3 scripts/dashboard.py
python3 scripts/redis_workflow.py deliver c1
python3 scripts/dashboard.py
```

### MongoDB — Historique et analyses

```bash
python3 scripts/init_mongo.py
python3 scripts/mongo_queries.py
```

### Synchronisation Redis → MongoDB

```bash
python3 scripts/init_redis.py
python3 scripts/init_mongo.py
python3 scripts/redis_workflow.py assign c1 d3
python3 scripts/sync_redis_to_mongo.py c1
```

---

## Interface web MongoDB

Accédez à l'interface d'administration via votre navigateur :

| Paramètre    | Valeur                        |
|--------------|-------------------------------|
| URL          | http://localhost:8081         |
| Utilisateur  | `admin`                       |
| Mot de passe | `pass`                        |

**Base de données :** `projet_livraison`  
**Collection :** `historique_livraison`

> Permet de visualiser les livraisons archivées depuis Redis.

---

## Résumé des fonctionnalités

| Fonctionnalité               | Outil       |
|------------------------------|-------------|
| Gestion temps réel           | Redis       |
| Analyse historique           | MongoDB     |
| Synchronisation inter-systèmes | Redis → MongoDB |
| Optimisation & géolocalisation | Cache + geo_logic |
