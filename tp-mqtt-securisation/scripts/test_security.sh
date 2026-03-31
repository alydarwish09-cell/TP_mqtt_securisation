#!/bin/bash
# ============================================================
# Script de tests de sécurité MQTT
# TP Sécurisation MQTT - IPSSI MSC Cybersécurité
# ============================================================

BROKER="localhost"
CERTS_DIR="./mosquitto/certs"

echo "======================================================"
echo "  Tests de Sécurité MQTT - TP IoT IPSSI"
echo "======================================================"
echo ""

# -------------------------------------------------------
# TEST 1 : Accès anonyme (doit ÉCHOUER)
# -------------------------------------------------------
echo "[TEST 1] Connexion anonyme (doit échouer - accès refusé)"
mosquitto_pub -h "$BROKER" -p 1883 -t "test/topic" -m "Tentative anonyme" \
  2>&1 && echo "RÉSULTAT: ÉCHEC (connexion autorisée - PROBLÈME DE SÉCURITÉ)" \
  || echo "RÉSULTAT: SUCCÈS (connexion refusée comme attendu)"
echo ""

# -------------------------------------------------------
# TEST 2 : Authentification avec identifiants valides (doit RÉUSSIR)
# -------------------------------------------------------
echo "[TEST 2] Connexion avec authentification valide (user1)"
mosquitto_pub -h "$BROKER" -p 1883 -u "user1" -P "Password123!" \
  -t "test/topic" -m "Message authentifié" 2>&1 \
  && echo "RÉSULTAT: SUCCÈS (connexion authentifiée)" \
  || echo "RÉSULTAT: ÉCHEC (vérifier le broker)"
echo ""

# -------------------------------------------------------
# TEST 3 : Authentification avec mauvais mot de passe (doit ÉCHOUER)
# -------------------------------------------------------
echo "[TEST 3] Connexion avec mauvais mot de passe (doit échouer)"
mosquitto_pub -h "$BROKER" -p 1883 -u "user1" -P "mauvaismdp" \
  -t "test/topic" -m "Test mauvais mdp" 2>&1 \
  && echo "RÉSULTAT: ÉCHEC (connexion autorisée - PROBLÈME DE SÉCURITÉ)" \
  || echo "RÉSULTAT: SUCCÈS (connexion refusée comme attendu)"
echo ""

# -------------------------------------------------------
# TEST 4 : Connexion TLS (port 8883)
# -------------------------------------------------------
echo "[TEST 4] Connexion sécurisée TLS sur port 8883"
mosquitto_pub -h "$BROKER" -p 8883 \
  --cafile "$CERTS_DIR/ca.crt" \
  -u "user1" -P "Password123!" \
  -t "test/topic" -m "Message TLS" 2>&1 \
  && echo "RÉSULTAT: SUCCÈS (connexion TLS établie)" \
  || echo "RÉSULTAT: ÉCHEC (vérifier les certificats et le broker)"
echo ""

# -------------------------------------------------------
# TEST 5 : Violation ACL - sensor_node_1 publie hors de son périmètre (doit ÉCHOUER)
# -------------------------------------------------------
echo "[TEST 5] Violation ACL - sensor_node_1 tente de publier sur home/sensor2 (doit échouer)"
mosquitto_pub -h "$BROKER" -p 1883 \
  -u "sensor_node_1" -P "Sensor@2024" \
  -t "home/sensor2/temperature" -m "Injection de données" 2>&1 \
  && echo "RÉSULTAT: VÉRIFIER LES LOGS (message envoyé mais doit être bloqué par ACL)" \
  || echo "RÉSULTAT: CONNEXION REFUSÉE"
echo ""

# -------------------------------------------------------
# TEST 6 : mTLS - Connexion avec certificat client
# -------------------------------------------------------
echo "[TEST 6] Connexion mTLS avec certificat client"
mosquitto_pub -h "$BROKER" -p 8883 \
  --cafile "$CERTS_DIR/ca.crt" \
  --cert "$CERTS_DIR/client.crt" \
  --key "$CERTS_DIR/client.key" \
  -u "user1" -P "Password123!" \
  -t "test/topic" -m "Message mTLS" 2>&1 \
  && echo "RÉSULTAT: SUCCÈS (connexion mTLS établie)" \
  || echo "RÉSULTAT: ÉCHEC (vérifier la configuration require_certificate)"
echo ""

echo "======================================================"
echo "  Fin des tests"
echo "======================================================"
