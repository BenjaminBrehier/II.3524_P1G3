# Outil de Hacking

Bienvenue dans l'outil de hacking. Cet outil est conçu pour des tests de sécurité uniquement. Utilisez-le de manière responsable et uniquement sur des systèmes pour lesquels vous avez l'autorisation.

## Installation

Pour installer les dépendances nécessaires, exécutez la commande suivante :

```bash
pip install -r requirements.txt
```

## Configuration

Pour utiliser Vulnerable Components, vous devez définir la variable d'environnement `GITHUB_TOKEN` avec un token valide.

```bash
export GITHUB_TOKEN="YOUR_GITHUB_TOKEN"
```

Attention : L'attaque ICMP DDOS nécessite un accès root

## Ressources

- Le fichier csrf.php est un exemple de fichier serveur vulnérable.
- Le fichier subdomainsPossibilites.txt est un exemple de fichier contenant des sous-domaines possibles.
- Le dossier enTest-XSS_SQLi contient des exemples de fichiers vulnérables pour les attaques XSS et SQLi.
- Le dossier Dictionnaire contient des dictionnaires de mots de passe pour l'attaque par force brute.
