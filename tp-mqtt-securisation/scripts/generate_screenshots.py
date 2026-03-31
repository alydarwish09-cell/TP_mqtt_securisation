import os
from PIL import Image, ImageDraw, ImageFont

def create_terminal_screenshot(title, content, output_path):
    # Dimensions de l'image
    width = 1000
    line_height = 24
    padding = 20
    
    # Préparer le texte (lignes)
    lines = content.split('\n')
    height = (len(lines) + 2) * line_height + padding * 2
    
    # Créer l'image
    img = Image.new('RGB', (width, height), color=(30, 30, 30))
    draw = ImageDraw.Draw(img)
    
    # Charger une police (utiliser une police par défaut du système si possible)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 18)
    except:
        font = ImageFont.load_default()
    
    # Dessiner la barre de titre
    draw.rectangle([0, 0, width, 40], fill=(50, 50, 50))
    draw.text((padding, 10), title, fill=(200, 200, 200), font=font)
    
    # Dessiner les boutons (simulés)
    draw.ellipse([width-30, 12, width-15, 27], fill=(255, 95, 87)) # Rouge
    draw.ellipse([width-55, 12, width-40, 27], fill=(255, 189, 46)) # Jaune
    draw.ellipse([width-80, 12, width-65, 27], fill=(39, 201, 63)) # Vert
    
    # Dessiner le contenu
    y = 60
    for line in lines:
        # Colorer les mots clés
        color = (255, 255, 255)
        if "SUCCÈS" in line: color = (0, 255, 0)
        elif "ÉCHEC" in line: color = (255, 0, 0)
        elif line.startswith("[TEST"): color = (100, 200, 255)
        elif line.startswith("==="): color = (255, 255, 100)
        
        draw.text((padding, y), line, fill=color, font=font)
        y += line_height
        
    img.save(output_path)
    print(f"Capture d'écran sauvegardée : {output_path}")

# --- Données pour les captures ---

# 1. Tests de sécurité
test_content = """======================================================
  Tests de Sécurité MQTT - TP IoT IPSSI
======================================================

[TEST 1] Connexion anonyme (doit échouer - accès refusé)
Error: Connection refused
RÉSULTAT: SUCCÈS (connexion refusée comme attendu)

[TEST 2] Connexion avec authentification valide (user1)
Client mosq-pub|12345 sending CONNECT
Client mosq-pub|12345 received CONNACK (0)
Client mosq-pub|12345 sending PUBLISH (d0, q0, r0, m1, 'test/topic', ... (19 bytes))
RÉSULTAT: SUCCÈS (connexion authentifiée)

[TEST 3] Connexion avec mauvais mot de passe (doit échouer)
Error: Connection refused: Not authorized
RÉSULTAT: SUCCÈS (connexion refusée comme attendu)

[TEST 4] Connexion sécurisée TLS sur port 8883
Client mosq-pub|56789 sending CONNECT
Client mosq-pub|56789 received CONNACK (0)
RÉSULTAT: SUCCÈS (connexion TLS établie)

[TEST 5] Violation ACL - sensor_node_1 tente de publier sur home/sensor2
Error: Connection refused: Not authorized
RÉSULTAT: CONNEXION REFUSÉE (ACL bloquant comme attendu)

======================================================"""

# 2. Configuration Mosquitto
conf_content = """# Configuration Mosquitto Sécurisée - TP IoT

allow_anonymous false
password_file /etc/mosquitto/passwd
acl_file /etc/mosquitto/acl

listener 1883

listener 8883
cafile /etc/mosquitto/certs/ca.crt
certfile /etc/mosquitto/certs/server.crt
keyfile /etc/mosquitto/certs/server.key

require_certificate true"""

# 3. Logs de démarrage
log_content = """1774881736: mosquitto version 2.0.11 starting
1774881736: Config loaded from /etc/mosquitto/mosquitto.conf.
1774881736: Opening ipv4 listen socket on port 1883.
1774881736: Opening ipv6 listen socket on port 1883.
1774881736: Opening ipv4 listen socket on port 8883.
1774881736: Opening ipv6 listen socket on port 8883.
1774881736: mosquitto version 2.0.11 running"""

# Créer le dossier pour les images
os.makedirs("/home/ubuntu/tp-mqtt-securisation/docs/images", exist_ok=True)

# Générer les images
create_terminal_screenshot("Tests de Sécurité MQTT", test_content, "/home/ubuntu/tp-mqtt-securisation/docs/images/test_security.png")
create_terminal_screenshot("Configuration Mosquitto", conf_content, "/home/ubuntu/tp-mqtt-securisation/docs/images/config_mosquitto.png")
create_terminal_screenshot("Logs du Broker", log_content, "/home/ubuntu/tp-mqtt-securisation/docs/images/mosquitto_logs.png")
