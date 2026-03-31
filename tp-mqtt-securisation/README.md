# TP Sécurisation MQTT pour l'IoT

**Cours :** IPSSI MSC Cybersécurité - Sécurisation IoT
**Etudiant :** Aly DARWISH
**Date :** 30 Mars 2026

## Objectifs

Ce TP couvre l'installation, la configuration et la sécurisation d'un broker MQTT Mosquitto dans un contexte IoT. Les mécanismes de sécurité mis en œuvre sont :

- Authentification par mot de passe (désactivation de l'accès anonyme)
- Chiffrement des communications via TLS (port 8883)
- Authentification mutuelle mTLS (certificat client)
- Contrôle d'accès par topic via ACL
- Déploiement reproductible via Docker Compose

## Structure du Projet

```
tp-mqtt-securisation/
├── docker-compose.yml          # Déploiement Docker Compose
├── .gitignore                  # Exclusions Git (clés privées, logs)
├── README.md                   # Ce fichier
├── mosquitto/
│   ├── config/
│   │   ├── mosquitto.conf      # Configuration principale (Docker)
│   │   ├── mosquitto_native.conf # Configuration pour installation native
│   │   ├── passwd              # Fichier de mots de passe hashés
│   │   └── acl                 # Règles de contrôle d'accès
│   ├── certs/
│   │   ├── ca.crt              # Certificat de l'Autorité de Certification
│   │   ├── server.crt          # Certificat du broker
│   │   └── client.crt          # Certificat client (pour mTLS)
│   ├── data/                   # Données persistantes (ignoré par Git)
│   └── log/                    # Logs Mosquitto (ignoré par Git)
├── scripts/
│   ├── generate_certs.sh       # Génération des certificats TLS
│   ├── setup_users.sh          # Création des utilisateurs Mosquitto
│   └── test_security.sh        # Tests de sécurité automatisés
└── docs/
    └── Rapport_TP_MQTT.md      # Rapport complet avec réponses aux questions
```

## Prérequis

- Docker et Docker Compose installés
- `openssl` disponible sur le système
- `mosquitto-clients` pour les tests (`mosquitto_pub`, `mosquitto_sub`)

## Démarrage Rapide

### 1. Générer les certificats TLS

```bash
chmod +x scripts/generate_certs.sh
bash scripts/generate_certs.sh
```

### 2. Lancer le broker via Docker Compose

```bash
docker-compose up -d
docker-compose logs -f
```

### 3. Vérifier que le broker écoute

```bash
ss -tulnp | grep -E "1883|8883"
```

### 4. Lancer les tests de sécurité

```bash
chmod +x scripts/test_security.sh
bash scripts/test_security.sh
```

## Utilisateurs Configurés

| Utilisateur | Rôle | Topics autorisés |
|-------------|------|-----------------|
| `user1` | Utilisateur de test | `readwrite test/#`, `read maison/temperature` |
| `sensor_node_1` | Capteur IoT | `readwrite home/sensor1/#` |
| `dashboard` | Tableau de bord | `read home/#` |
| `admin` | Administrateur | `readwrite #` |

> **Note :** Les mots de passe sont stockés hashés dans `mosquitto/config/passwd`. Ne jamais versionner les clés privées (`.key`).

## Ports Exposés

| Port | Protocole | Description |
|------|-----------|-------------|
| 1883 | MQTT | Non chiffré (tests internes uniquement) |
| 8883 | MQTT/TLS | Chiffré avec certificats |
| 9001 | WebSocket | WebSocket MQTT (si activé) |

## Tests Manuels

### Test de connexion anonyme (doit échouer)
```bash
mosquitto_pub -h localhost -t test -m "anon"
```

### Test avec authentification
```bash
mosquitto_pub -h localhost -u user1 -P Password123! -t test/topic -m "auth"
```

### Test TLS
```bash
mosquitto_pub -p 8883 --cafile mosquitto/certs/ca.crt \
  -u user1 -P Password123! -t test/topic -m "tls"
```

### Test mTLS (authentification mutuelle)
```bash
mosquitto_pub -p 8883 \
  --cafile mosquitto/certs/ca.crt \
  --cert mosquitto/certs/client.crt \
  --key mosquitto/certs/client.key \
  -u user1 -P Password123! -t test/topic -m "mtls"
```

## Surveillance et Diagnostic

```bash
# Logs en temps réel
journalctl -u mosquitto -f

# Firewall - autoriser le port TLS
sudo ufw allow 8883

# Vérifier les connexions actives
ss -tulnp | grep 1883
```

## Rapport

Le rapport complet avec les réponses aux questions se trouve dans [`docs/Rapport_TP_MQTT.md`](docs/Rapport_TP_MQTT.md).
