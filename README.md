# Passager (Password Manager)

Ce projet est un gestionnaire de mots de passe simple et efficace, construit avec Python et Tkinter. Il permet de générer des mots de passe sécurisés pour différents sites et de les stocker de manière sécurisée. L'utilisateur peut aussi y renseigner ses propres mots de passe ou modifier les mots de passe générés.

## Fonctionnalités

- Génération de mots de passe sécurisés
- Stockage sécurisé des mots de passe par chiffrement AES. Le mot de passe principal, servant à chiffrer le fichier, n'est pas stocké en clair.
- Interface utilisateur simple et intuitive.

## Installation

1. Clonez ce dépôt sur votre machine locale : `https://github.com/milairhu/passager.git`
2. Installez les dépendances avec la commande `pip install -r requirements.txt`.
3. Exécutez le fichier `main.py` pour lancer l'application.

## Utilisation

Lors du premier lancement de l'application, l'utilistaeur est invité à créer un mot de passe principal. Ce mot de passe sera utilisé pour accéder à l'application à l'avenir. **ATTENTION :** Si vous perdez ce mot de passe, vous ne pourrez plus accéder à vos mots de passe stockés.

Une fois que le mot de passe principal est défini, dans un premier onglet l'utilisateur peut générer et stocker des mots de passe pour différents sites. Entrez simplement l'URL du site et cliquez sur "Générer / Chercher le mdp".

Dans un second onglet, l'utilisateur peut renseigner ses propres mots de passe ou modifier les mots de passe générés.

## Améliorations souhaitables

- Ajouter un système de vérification de la force du mot de passe principal et des mots de passes ajoutés manuellement.
- Ajouter un système de récupération de mot de passe principal, via adresse mail par exemple.
- Prévenir les attaques par force brute sur le mot de passe principal avec un nombre d'essais limité.

Les deux derniers points n'ont pas été réalisé, car on n'a pas trouvé meilleure solution que de stocker l'adresse email et le nombre de tentatives dans un fichier non chiffré, ce qui présente une faille de sécurité majeure. Il aurait presque été préférable d'implémenter l'auto-destruction du fichier chiffré en cas de tentative d'attaque par force brute.
