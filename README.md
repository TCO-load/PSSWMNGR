# 🔐 Gestionnaire de Mots de Passe Sécurisé

Un gestionnaire de mots de passe portable, sécurisé et facile à utiliser, conçu pour être stocké sur une clé USB.

![psswd](https://github.com/user-attachments/assets/33c87a75-9507-4d6c-8ff2-a6ee7a5eacfd)



## ✨ Caractéristiques

- 🛡️ Stockage sécurisé des mots de passe avec chiffrement
- 🎲 Génération de mots de passe aléatoires robustes
- 🔑 Protection par mot de passe maître
- 🌈 Interface colorée
- ⏰ Avertissement pour les mots de passe de plus de 6 mois
- 💾 Portable et facile à utiliser sur n'importe quel ordinateur avec Python

## 🛠️ Prérequis

- Python 3.6 ou supérieur
- Bibliothèques requises : cryptography

## 🚀 Installation

1. Clonez ce dépôt ou téléchargez le fichier `password_manager.py` + start PSWD.bat sur votre clé USB.

## 🔧 Utilisation

1. Connectez votre clé USB à l'ordinateur.

2. Exécutez le script :
start PSWD.bat

4. Lors de la première utilisation, vous serez invité à créer un mot de passe maître.

5. Utilisez le menu pour gérer vos mots de passe :
- ➕ Ajouter un nouveau mot de passe
- 🎲 Générer un mot de passe aléatoire
- 👀 Voir un mot de passe existant
- 🔄 Mettre à jour un mot de passe
- 🗑️ Supprimer un mot de passe
- 🔑 Changer le mot de passe maître


## 🔒 Sécurité

- Tous les mots de passe sont chiffrés à l'aide de Fernet (AES)
- Le mot de passe maître est protégé par un hachage sécurisé
- La génération de mots de passe utilise la bibliothèque `secrets` de Python

## 🎨 Personnalisation

Vous pouvez ajuster le chemin de la clé USB en modifiant la variable `usb_path` dans la fonction `main()`.

## 👥 Contribution

Les contributions à ce projet sont les bienvenues. N'hésitez pas à ouvrir une issue ou à soumettre une pull request.

## 👤 Auteur

Titouan Cornille

## 📜 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🙏 Remerciements

- Merci à tous les contributeurs et utilisateurs de ce projet.
- Inspiré par les meilleures pratiques en matière de gestion de mots de passe.
