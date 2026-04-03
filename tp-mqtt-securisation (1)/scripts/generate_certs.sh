#!/bin/bash
# ============================================================
# Script de génération des certificats TLS pour Mosquitto
# TP Sécurisation MQTT - IPSSI MSC Cybersécurité
# ============================================================

set -e

CERTS_DIR="./mosquitto/certs"
mkdir -p "$CERTS_DIR"

echo "[1/4] Génération de la clé et du certificat de l'Autorité de Certification (CA)..."
openssl genrsa -out "$CERTS_DIR/ca.key" 2048
openssl req -new -x509 -days 3650 -key "$CERTS_DIR/ca.key" -out "$CERTS_DIR/ca.crt" \
  -subj "/C=FR/ST=IleDeFrance/L=Paris/O=IPSSI/OU=Cybersecurite/CN=IPSSI-CA"

echo "[2/4] Génération de la clé et du certificat du serveur (broker)..."
openssl genrsa -out "$CERTS_DIR/server.key" 2048
openssl req -new -key "$CERTS_DIR/server.key" -out "$CERTS_DIR/server.csr" \
  -subj "/C=FR/ST=IleDeFrance/L=Paris/O=IPSSI/OU=Cybersecurite/CN=localhost"
openssl x509 -req -days 365 -in "$CERTS_DIR/server.csr" \
  -CA "$CERTS_DIR/ca.crt" -CAkey "$CERTS_DIR/ca.key" -CAcreateserial \
  -out "$CERTS_DIR/server.crt"

echo "[3/4] Génération de la clé et du certificat du client (pour mTLS)..."
openssl genrsa -out "$CERTS_DIR/client.key" 2048
openssl req -new -key "$CERTS_DIR/client.key" -out "$CERTS_DIR/client.csr" \
  -subj "/C=FR/ST=IleDeFrance/L=Paris/O=IPSSI/OU=Cybersecurite/CN=client-user1"
openssl x509 -req -days 365 -in "$CERTS_DIR/client.csr" \
  -CA "$CERTS_DIR/ca.crt" -CAkey "$CERTS_DIR/ca.key" -CAcreateserial \
  -out "$CERTS_DIR/client.crt"

echo "[4/4] Vérification des certificats..."
echo "--- Certificat CA ---"
openssl x509 -in "$CERTS_DIR/ca.crt" -noout -subject -issuer -dates
echo "--- Certificat Serveur ---"
openssl x509 -in "$CERTS_DIR/server.crt" -noout -subject -issuer -dates
echo "--- Certificat Client ---"
openssl x509 -in "$CERTS_DIR/client.crt" -noout -subject -issuer -dates

echo ""
echo "Certificats générés avec succès dans $CERTS_DIR"
