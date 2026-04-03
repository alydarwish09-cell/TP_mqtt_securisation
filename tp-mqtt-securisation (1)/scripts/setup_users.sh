#!/bin/bash
# ============================================================
# Script de création des utilisateurs Mosquitto
# TP Sécurisation MQTT - IPSSI MSC Cybersécurité
# ============================================================
# Usage: sudo bash setup_users.sh
# ============================================================

PASSWD_FILE="/etc/mosquitto/passwd"

echo "[1/4] Création de l'utilisateur user1 (utilisateur de test)..."
sudo mosquitto_passwd -c -b "$PASSWD_FILE" user1 Password123!

echo "[2/4] Création de l'utilisateur sensor_node_1 (capteur IoT)..."
sudo mosquitto_passwd -b "$PASSWD_FILE" sensor_node_1 Sensor@2024

echo "[3/4] Création de l'utilisateur dashboard (tableau de bord)..."
sudo mosquitto_passwd -b "$PASSWD_FILE" dashboard Dashboard@2024

echo "[4/4] Création de l'utilisateur admin (administrateur)..."
sudo mosquitto_passwd -b "$PASSWD_FILE" admin Admin@Secure2024

echo ""
echo "Utilisateurs créés. Redémarrage du service Mosquitto..."
sudo systemctl restart mosquitto

echo "Configuration terminée. Vérification du statut:"
sudo systemctl status mosquitto --no-pager
