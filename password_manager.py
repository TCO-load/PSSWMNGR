import os
import sys
import json
import getpass
import secrets
import hashlib
import base64
import time
import uuid
import platform
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def purple(text):
    return f"\033[95m{text}\033[0m"

def green(text):
    return f"\033[92m{text}\033[0m"

def blue(text):
    return f"\033[94m{text}\033[0m"

def orange(text):
    return f"\033[93m{text}\033[0m"

def pink(text):
    return f"\033[95m{text}\033[0m"

def white(text):
    return f"\033[97m{text}\033[0m"
def get_usb_path():
    if platform.system() == "Windows":
        drive = input("Entrez la lettre du lecteur USB (ex: D): ")
        return f"{drive}:\\"  # Retourne le chemin complet, par exemple "D:\"
    elif platform.system() == "Linux":
        return input("Entrez le point de montage USB (ex: /media/username/USB_NAME): ")
    elif platform.system() == "Darwin":  # macOS
        return input("Entrez le chemin de la clé USB (ex: /Volumes/USB_NAME): ")
    else:
        raise NotImplementedError("Système d'exploitation non supporté")

class PasswordManager:
    def __init__(self, usb_path):
        self.usb_path = usb_path
        self.passwords_file = os.path.join(usb_path, "passwords.enc")
        self.master_file = os.path.join(usb_path, "master.json")
        self.id_file = os.path.join(usb_path, ".usb_id")
        self.key = None
        self.color_func = orange  # Couleur par défaut

    def clear_console(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_header(self, title):
        self.clear_console()
        print("=" * 50)
        print(self.color_func(f"{title:^50}"))
        print("=" * 50)
        print()

    def wait_for_user(self):
        input(self.color_func("\nAppuyez sur Entrée pour continuer..."))

    def show_banner(self):
            banner = f"""
    ╔═══════════════════════════════════════════════════════════════════════╗
    ║                                                                       ║
    ║   /$$$$$$$   /$$$$$$   /$$$$$$  /$$      /$$/$$$$$$$                  ║
    ║  | $$__  $$ /$$__  $$ /$$__  $$| $$  /$ | $| $$__  $$                 ║
    ║  | $$  \ $$| $$  \__/| $$  \__/| $$ /$$$| $| $$  \ $$                 ║
    ║  | $$$$$$$/|  $$$$$$ |  $$$$$$ | $$/$$ $$ $| $$  | $$                 ║
    ║  | $$____/  \____  $$ \____  $$| $$$$_  $$$| $$  | $$                 ║
    ║  | $$       /$$  \ $$ /$$  \ $$| $$$/ \  $$| $$  | $$                 ║
    ║  | $$      |  $$$$$$/|  $$$$$$/| $$/   \  $| $$$$$$$/                 ║
    ║  |__/       \______/  \______/ |__/     \__|_______/                  ║
    ║                                                                       ║
    ║               Gestionnaire de Mots de Passe Sécurisé                  ║
    ║                                                                       ║
    ║  [>] Running with Python {sys.version_info[0]}.{sys.version_info[1]}.{sys.version_info[2]}                                       ║
    ║  [>] GITHUB : TCO-load                                                ║
    ║                                                                       ║
    ╚═══════════════════════════════════════════════════════════════════════╝
    """
            print(self.color_func(banner))

    def initialize(self):
        if not os.path.exists(self.id_file):
            with open(self.id_file, 'w') as f:
                f.write(str(uuid.uuid4()))
        
        with open(self.id_file, 'r') as f:
            self.usb_id = f.read().strip()

        if not os.path.exists(self.master_file):
            self.print_header("Initialisation du gestionnaire de mots de passe")
            master_password = getpass.getpass(self.color_func("Créez un mot de passe maître: "))
            salt = os.urandom(16)
            key = self.derive_key(master_password, salt)
            
            master_data = {
                "salt": base64.b64encode(salt).decode('utf-8'),
                "verifier": base64.b64encode(hashlib.sha256(key).digest()).decode('utf-8')
            }
            
            with open(self.master_file, 'w') as f:
                json.dump(master_data, f)
            
            print(self.color_func("Gestionnaire de mots de passe initialisé avec succès."))
            self.wait_for_user()
        else:
            print(self.color_func("Gestionnaire de mots de passe déjà initialisé."))

    def login(self):
        self.print_header("Connexion")
        if not os.path.exists(self.master_file):
            print(self.color_func("Le gestionnaire de mots de passe n'est pas initialisé."))
            return False

        with open(self.master_file, 'r') as f:
            master_data = json.load(f)

        salt = base64.b64decode(master_data['salt'])
        stored_verifier = base64.b64decode(master_data['verifier'])

        master_password = getpass.getpass(self.color_func("Entrez votre mot de passe maître: "))
        key = self.derive_key(master_password, salt)
        
        if hashlib.sha256(key).digest() == stored_verifier:
            self.key = key
            return True
        else:
            print(self.color_func("Mot de passe maître incorrect."))
            self.wait_for_user()
            return False

    def show_animation(self):
        frames = [
            "F", "Fa", "Fai", "Fait", "Fait ", "Fait p", "Fait pa", "Fait par",
            "Fait par ", "Fait par T", "Fait par Ti", "Fait par Tit",
            "Fait par Tito", "Fait par Titou", "Fait par Titoua",
            "Fait par Titouan", "Fait par Titouan ", "Fait par Titouan C",
            "Fait par Titouan Co", "Fait par Titouan Cor", "Fait par Titouan Corn",
            "Fait par Titouan Corni", "Fait par Titouan Cornil",
            "Fait par Titouan Cornill", "Fait par Titouan Cornille",
        ]

        for frame in frames:
            self.clear_console()
            print("\n" * 10)
            print(self.color_func(frame.center(50)))
            time.sleep(0.1)
            
        time.sleep(1)
        self.clear_console()
        self.show_banner()
        time.sleep(4)
        
        
    def derive_key(self, password, salt):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))

    def add_password(self):
        self.print_header("Ajouter un mot de passe")
        platform = input(self.color_func("Nom de la plateforme: "))
        password = getpass.getpass(self.color_func("Mot de passe: "))
        
        passwords = self.load_passwords()
        passwords[platform] = {
            "password": password,
            "date": datetime.now().isoformat()
        }
        self.save_passwords(passwords)
        print(self.color_func(f"Mot de passe pour {platform} ajouté avec succès."))
        self.wait_for_user()

    def generate_password(self):
        self.print_header("Générer un mot de passe aléatoire")
        length = int(input(self.color_func("Longueur du mot de passe (8-32): ")))
        length = max(8, min(length, 32))
        password = ''.join(secrets.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=') for _ in range(length))
        print(self.color_func(f"Mot de passe généré: {password}"))
        
        save = input(self.color_func("Voulez-vous sauvegarder ce mot de passe? (o/n): ")).lower()
        if save == 'o':
            platform = input(self.color_func("Nom de la plateforme: "))
            passwords = self.load_passwords()
            passwords[platform] = {
                "password": password,
                "date": datetime.now().isoformat()
            }
            self.save_passwords(passwords)
            print(self.color_func(f"Mot de passe pour {platform} sauvegardé avec succès."))
        self.wait_for_user()

    def view_password(self):
        self.print_header("Voir un mot de passe")
        self.list_platforms()
        print("\n")
        platform = input(self.color_func("Entrez le nom de la plateforme (ou 'q' pour quitter): "))
        if platform.lower() == 'q':
            return

        passwords = self.load_passwords()
        if platform in passwords:
            print(self.color_func(f"\nPlateforme: {platform}"))
            print(self.color_func(f"Mot de passe: {passwords[platform]['password']}"))
            print(self.color_func(f"Date d'ajout: {passwords[platform]['date']}"))
        
            date_added = datetime.fromisoformat(passwords[platform]['date'])
            if datetime.now() - date_added > timedelta(days=180):
                print(self.color_func("ATTENTION: Ce mot de passe a plus de 6 mois."))
                update = input(self.color_func("Voulez-vous le mettre à jour? (o/n): ")).lower()
                if update == 'o':
                    self.update_password(platform)
        else:
            print(self.color_func("Plateforme non trouvée."))
        self.wait_for_user()
        
    def update_password(self, platform=None):
        self.print_header("Mettre à jour un mot de passe")
        if platform is None:
            platform = input(self.color_func("Nom de la plateforme à mettre à jour: "))
        
        passwords = self.load_passwords()
        if platform in passwords:
            new_password = getpass.getpass(self.color_func("Nouveau mot de passe: "))
            passwords[platform] = {
                "password": new_password,
                "date": datetime.now().isoformat()
            }
            self.save_passwords(passwords)
            print(self.color_func(f"Mot de passe pour {platform} mis à jour avec succès."))
        else:
            print(self.color_func("Plateforme non trouvée."))
        self.wait_for_user()

    def change_master_password(self):
        self.print_header("Changer le mot de passe maître")
        current_password = getpass.getpass(self.color_func("Entrez votre mot de passe maître actuel: "))
        with open(self.master_file, 'r') as f:
            master_data = json.load(f)
        
        salt = base64.b64decode(master_data['salt'])
        stored_verifier = base64.b64decode(master_data['verifier'])
        
        if hashlib.sha256(self.derive_key(current_password, salt)).digest() != stored_verifier:
            print(self.color_func("Mot de passe maître incorrect."))
            self.wait_for_user()
            return
        
        new_password = getpass.getpass(self.color_func("Nouveau mot de passe maître: "))
        confirm_password = getpass.getpass(self.color_func("Confirmez le nouveau mot de passe maître: "))
        
        if new_password != confirm_password:
            print(self.color_func("Les mots de passe ne correspondent pas."))
            self.wait_for_user()
            return
        
        new_salt = os.urandom(16)
        new_key = self.derive_key(new_password, new_salt)
        
        new_master_data = {
            "salt": base64.b64encode(new_salt).decode('utf-8'),
            "verifier": base64.b64encode(hashlib.sha256(new_key).digest()).decode('utf-8')
        }
        
        with open(self.master_file, 'w') as f:
            json.dump(new_master_data, f)
        
        self.key = new_key
        print(self.color_func("Mot de passe maître changé avec succès."))
        self.wait_for_user()

    def load_passwords(self):
        if not os.path.exists(self.passwords_file):
            return {}
        
        with open(self.passwords_file, 'rb') as f:
            encrypted_data = f.read()
        
        fernet = Fernet(self.key)
        decrypted_data = fernet.decrypt(encrypted_data)
        return json.loads(decrypted_data)

    def save_passwords(self, passwords):
        fernet = Fernet(self.key)
        encrypted_data = fernet.encrypt(json.dumps(passwords).encode())
        
        with open(self.passwords_file, 'wb') as f:
            f.write(encrypted_data)
            
    def list_platforms(self):
        passwords = self.load_passwords()
        if not passwords:
            print(self.color_func("Aucune plateforme enregistrée."))
        else:
            print(self.color_func("Plateformes enregistrées :"))
            for platform, data in passwords.items():
                date_added = datetime.fromisoformat(data['date'])
                days_old = (datetime.now() - date_added).days
                print(self.color_func(f"- {platform} (ajouté il y a {days_old} jours)"))
                if days_old > 180:
                    print(self.color_func("  ATTENTION: Ce mot de passe a plus de 6 mois."))
        print(self.color_func(f"\nTotal: {len(passwords)} plateforme(s)"))

    def change_color(self):
        self.print_header("Changer la couleur du texte")
        print(orange("1. Orange (par défaut)"))
        print(green("2. Vert"))
        print(blue("3. Bleu"))
        print(white("4. Blanc"))
        print(pink("5. Rose"))
        print(purple("6. Violet"))
        
        choice = input(self.color_func("Choisissez une couleur (1-6): "))
        
        if choice == '1':
            self.color_func = orange
        elif choice == '2':
            self.color_func = green
        elif choice == '3':
            self.color_func = blue
        elif choice == '4':
            self.color_func = white
        elif choice == '5':
            self.color_func = pink
        elif choice == '6':
            self.color_func = purple
        else:
            print(self.color_func("Choix invalide. La couleur reste inchangée."))
        
        print(self.color_func("Couleur changée avec succès."))
        self.wait_for_user()
        
    def delete_password(self):
        self.print_header("Supprimer un mot de passe")
        self.list_platforms()
        print("\n")
        platform = input(self.color_func("Entrez le nom de la plateforme à supprimer (ou 'q' pour quitter): "))
        if platform.lower() == 'q':
            return

        passwords = self.load_passwords()
        if platform in passwords:
            confirm = input(self.color_func(f"Êtes-vous sûr de vouloir supprimer le mot de passe pour {platform}? (o/n): ")).lower()
            if confirm == 'o':
                del passwords[platform]
                self.save_passwords(passwords)
                print(self.color_func(f"Mot de passe pour {platform} supprimé avec succès."))
            else:
                print(self.color_func("Suppression annulée."))
        else:
            print(self.color_func("Plateforme non trouvée."))
        self.wait_for_user()

def main():
    usb_path = get_usb_path()
    
    if not os.path.exists(usb_path):
        print(orange("Chemin USB non valide. Veuillez vérifier votre clé USB."))
        return
    
    pm = PasswordManager(usb_path)
    
    pm.initialize()
    pm.show_animation()
    
    if not pm.login():
        print(pm.color_func("Échec de l'authentification. Au revoir!"))
        return
    
    while True:
        pm.clear_console()
        pm.show_banner()
        print(pm.color_func("[1]. Ajouter un mot de passe"))
        print(pm.color_func("[2]. Générer un mot de passe aléatoire"))
        print(pm.color_func("[3]. Voir un mot de passe"))
        print(pm.color_func("[4]. Mettre à jour un mot de passe"))
        print(pm.color_func("[5]. Supprimer un mot de passe"))
        print(pm.color_func("[6]. Changer le mot de passe maître"))
        print(pm.color_func("[7]. Changer la couleur du texte"))
        print(pm.color_func("[8]. Quitter"))
        print()
        
        choice = input(pm.color_func("Choisissez une option (1-8): "))
        
        if choice == '1':
            pm.add_password()
        elif choice == '2':
            pm.generate_password()
        elif choice == '3':
            pm.view_password()
        elif choice == '4':
            pm.update_password()
        elif choice == '5':
            pm.delete_password()
        elif choice == '6':
            pm.change_master_password()
        elif choice == '7':
            pm.change_color()
        elif choice == '8':
            pm.clear_console()
            print(pm.color_func("Merci d'avoir utilisé le gestionnaire de mots de passe. Au revoir!"))
            break
        else:
            print(pm.color_func("Option invalide. Veuillez réessayer."))
            pm.wait_for_user()

if __name__ == "__main__":
    main()