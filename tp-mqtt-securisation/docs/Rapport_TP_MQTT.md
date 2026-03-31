# Rapport de TP : Sécurisation MQTT pour l'IoT

**Etudiant :** Aly DARWISH
**Date :** 30 Mars 2026
**Sujet :** Installation, Configuration et Sécurisation MQTT sur Ubuntu

## Introduction

Ce rapport présente les résultats du TP sur la sécurisation d'un broker MQTT (Mosquitto) dans un environnement IoT. L'objectif principal était de comprendre les enjeux de sécurité liés au protocole MQTT et de mettre en œuvre des mécanismes de protection tels que l'authentification, le chiffrement TLS et les listes de contrôle d'accès (ACL).

## 1. Tableau des Vulnérabilités et Mitigations

Le tableau ci-dessous résume les risques identifiés, les mesures de mitigation proposées, ainsi que les défis liés à leur mise en œuvre.

| Vulnérabilité | Risque | Mitigation | Challenges / Obstacles |
|---------------|--------|------------|------------------------|
| **Pas d'authentification (accès anonyme)** | Usurpation d'identité, injection de données malveillantes, saturation du broker (DDoS). | Désactiver l'accès anonyme (`allow_anonymous false`) et exiger un mot de passe (`password_file`). | Gestion sécurisée des mots de passe sur les objets connectés ayant des ressources limitées. Mise à jour complexe des identifiants sur une flotte d'appareils déployés. |
| **MQTT en clair (sans chiffrement)** | Interception des données (Man-In-The-Middle), vol d'identifiants transmis en clair, violation de confidentialité. | Utiliser le chiffrement TLS sur le port 8883 (`listener 8883` avec certificats). | Les calculs cryptographiques du TLS consomment des ressources CPU et de la batterie sur les petits capteurs IoT. La gestion et le renouvellement des certificats (PKI) sont complexes à l'échelle. |
| **Topics permissifs (pas de restriction)** | Un capteur compromis peut publier des fausses commandes (ex: déverrouiller une porte) ou lire des données sensibles d'autres capteurs. | Mettre en place des ACL (`acl_file`) pour restreindre les droits de lecture/écriture par utilisateur et par topic. | Nécessite une cartographie précise des flux de données. La configuration des règles peut devenir lourde et sujette à erreurs si le nombre de capteurs et de topics est important. |

## 2. Réponses aux Questions

### Question 1 : Quels sont les risques si MQTT n'est pas sécurisé ?

Si le protocole MQTT est déployé sans mécanismes de sécurité (port 1883 par défaut), l'ensemble du réseau IoT est exposé à de multiples menaces :
- **Man-In-The-Middle (MitM) :** Toutes les données (y compris les mots de passe si envoyés en clair) peuvent être interceptées. Cela pose un risque majeur pour la confidentialité des données des utilisateurs.
- **Injection et altération de données :** Un attaquant peut publier de fausses valeurs de capteurs (ex: fausse température pour déclencher un incendie) ou envoyer des commandes malveillantes aux actionneurs.
- **Déni de service (DoS) :** Sans restriction, un attaquant peut inonder le broker de messages, saturant la bande passante ou la mémoire, rendant le système indisponible.
- **Prise de contrôle :** L'absence d'authentification permet à n'importe qui de s'abonner aux topics système (`$SYS`) pour obtenir des informations sur l'infrastructure ou de prendre le contrôle d'appareils critiques.

### Question 2 : Quelle est la différence entre TLS et mTLS ?

- **TLS (Transport Layer Security) standard :** C'est une authentification unidirectionnelle. Le serveur (broker MQTT) présente son certificat au client (capteur IoT). Le client vérifie l'identité du serveur et un canal chiffré est établi. Cela garantit la confidentialité et protège contre le MitM, mais le serveur ne sait pas cryptographiquement qui est le client (il s'appuie souvent sur un login/mot de passe par-dessus TLS).
- **mTLS (Mutual TLS) :** C'est une authentification bidirectionnelle. Non seulement le client vérifie le certificat du serveur, mais le client doit également présenter son propre certificat valide au serveur. Le broker MQTT n'accepte la connexion que si le certificat du client est signé par une Autorité de Certification (CA) de confiance. Cela offre un niveau de sécurité "Zero Trust" très élevé, idéal pour l'IoT (machine-to-machine), supprimant le besoin de mots de passe vulnérables.

### Question 3 : Pourquoi utiliser des ACL (Access Control Lists) ?

Les ACL permettent de mettre en œuvre le principe de **moindre privilège**. Dans un réseau IoT, un capteur de température ne devrait avoir le droit que de publier sur son propre topic de température, et n'a aucune raison de pouvoir lire les commandes d'ouverture de porte ou de publier sur le topic d'un autre capteur. 

L'utilisation d'ACL permet de :
- **Cloisonner les accès :** Si un capteur est compromis physiquement ou logiquement, l'attaquant ne pourra agir que dans le périmètre restreint défini par l'ACL de ce capteur.
- **Protéger l'infrastructure :** Empêcher les clients standards d'accéder aux topics de supervision (`$SYS/#`).
- **Structurer les flux :** Séparer clairement les rôles (ex: les capteurs publient, les tableaux de bord lisent).

## 3. Mise en œuvre et Vérification

### 3.1 Configuration du Broker Mosquitto

La configuration du broker Mosquitto (`mosquitto.conf`) a été adaptée pour désactiver l'accès anonyme, activer l'authentification par mot de passe, et configurer le chiffrement TLS sur le port 8883. Les chemins vers les fichiers de mots de passe, ACL et certificats sont spécifiés.

![Configuration Mosquitto](images/config_mosquitto.png)

### 3.2 Logs de Démarrage du Broker

Les logs de démarrage du broker Mosquitto confirment que les listeners sur les ports 1883 (non sécurisé) et 8883 (sécurisé TLS) sont bien ouverts et que la configuration a été chargée avec succès.

![Logs du Broker](images/mosquitto_logs.png)

### 3.3 Tests de Sécurité

Des tests ont été effectués pour valider la mise en place des mécanismes de sécurité. Les résultats montrent que l'accès anonyme est refusé, l'authentification par mot de passe fonctionne, et les connexions TLS sont établies. Les ACL bloquent également les tentatives de publication non autorisées.

![Tests de Sécurité MQTT](images/test_security.png)

## Conclusion

La sécurisation d'un environnement MQTT nécessite une approche en profondeur (Defense in Depth) : chiffrement des communications (TLS), authentification forte (mTLS ou mots de passe robustes), et contrôle d'accès strict (ACL). Le déploiement via Docker Compose facilite la gestion de ces configurations de manière reproductible et isolée.

