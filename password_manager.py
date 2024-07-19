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
import shutil
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from colorama import Fore, Style, init

init(autoreset=True)

class PasswordManager:
    def __init__(self, usb_path):
        self.usb_path = usb_path
        self.passwords_file = os.path.join(usb_path, "passwords.enc")
        self.master_file = os.path.join(usb_path, "master.json")
        self.id_file = os.path.join(usb_path, ".usb_id")
        self.key = None
        self.terminal_width = shutil.get_terminal_size().columns

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def center_text(self, text):
        return text.center(self.terminal_width)

    def print_centered(self, text, color=Fore.WHITE):
        print(color + self.center_text(text) + Style.RESET_ALL)

    def print_banner(self):
        banner = '''
    /$$$$$$$   /$$$$$$   /$$$$$$  /$$      /$$/$$$$$$$  
    | $$__  $$ /$$__  $$ /$$__  $$| $$  /$ | $| $$__  $$ 
    | $$  \ $$| $$  \__/| $$  \__/| $$ /$$$| $| $$  \ $$ 
    | $$$$$$$/|  $$$$$$ |  $$$$$$ | $$/$$ $$ $| $$  | $$ 
    | $$____/  \____  $$ \____  $$| $$$$_  $$$| $$  | $$ 
    | $$       /$$  \ $$ /$$  \ $$| $$$/ \  $$| $$  | $$ 
   | $$      |  $$$$$$/|  $$$$$$/| $$/   \  $| $$$$$$$/
   |__/       \______/  \______/ |__/     \__|_______/ 
    '''
        for line in banner.split('\n'):
            self.print_centered(line, Fore.RED)
        self.print_centered("Gestionnaire de Mots de Passe Sécurisé", Fore.CYAN)
        self.print_centered("=" * 45, Fore.YELLOW)

    def print_menu(self, title, options):
        self.clear_screen()
        self.print_banner()
        print()
        self.print_centered(title, Fore.CYAN + Style.BRIGHT)
        self.print_centered("=" * (len(title) + 4), Fore.YELLOW)
        for i, option in enumerate(options, 1):
            self.print_centered(f"{i}. {option}", Fore.GREEN)
        self.print_centered("=" * (len(title) + 4), Fore.YELLOW)

    def get_user_input(self, prompt):
        return input(prompt)

    def get_password(self, prompt):
        return getpass.getpass(prompt)

    def get_user_choice(self, max_choice):
        while True:
            try:
                choice = int(self.get_user_input(f"{Fore.CYAN}Choisissez une option (1-{max_choice}): {Style.RESET_ALL}"))
                if 1 <= choice <= max_choice:
                    return choice
                else:
                    self.print_centered(f"Choix invalide. Veuillez entrer un nombre entre 1 et {max_choice}.", Fore.RED)
            except ValueError:
                self.print_centered("Entrée invalide. Veuillez entrer un nombre.", Fore.RED)

    def initialize(self):
        if not os.path.exists(self.id_file):
            with open(self.id_file, 'w') as f:
                f.write(str(uuid.uuid4()))
        
        with open(self.id_file, 'r') as f:
            self.usb_id = f.read().strip()

        if not os.path.exists(self.master_file):
            self.print_centered("Initialisation du gestionnaire de mots de passe", Fore.CYAN)
            master_password = self.get_password(f"{Fore.GREEN}Créez un mot de passe maître: {Style.RESET_ALL}")
            salt = os.urandom(16)
            key = self.derive_key(master_password, salt)
            
            master_data = {
                "salt": base64.b64encode(salt).decode('utf-8'),
                "verifier": base64.b64encode(hashlib.sha256(key).digest()).decode('utf-8')
            }
            
            with open(self.master_file, 'w') as f:
                json.dump(master_data, f)
            
            self.print_centered("Gestionnaire de mots de passe initialisé avec succès.", Fore.GREEN)
            self.get_user_input(f"{Fore.CYAN}Appuyez sur Entrée pour continuer...{Style.RESET_ALL}")
        else:
            self.print_centered("Gestionnaire de mots de passe déjà initialisé.", Fore.YELLOW)

    def login(self):
        self.print_centered("Connexion", Fore.CYAN)
        if not os.path.exists(self.master_file):
            self.print_centered("Le gestionnaire de mots de passe n'est pas initialisé.", Fore.RED)
            return False

        with open(self.master_file, 'r') as f:
            master_data = json.load(f)

        salt = base64.b64decode(master_data['salt'])
        stored_verifier = base64.b64decode(master_data['verifier'])

        master_password = self.get_password(f"{Fore.GREEN}Entrez votre mot de passe maître: {Style.RESET_ALL}")
        key = self.derive_key(master_password, salt)
        
        if hashlib.sha256(key).digest() == stored_verifier:
            self.key = key
            return True
        else:
            self.print_centered("Mot de passe maître incorrect.", Fore.RED)
            self.get_user_input(f"{Fore.CYAN}Appuyez sur Entrée pour continuer...{Style.RESET_ALL}")
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
            self.clear_screen()
            print("\n" * 10)
            self.print_centered(frame, Fore.CYAN)
            time.sleep(0.1)
            
        time.sleep(1)
        self.clear_screen()
        self.print_banner()
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
        self.print_menu("Ajouter un mot de passe", [])
        platform = self.get_user_input(f"{Fore.GREEN}Nom de la plateforme: {Style.RESET_ALL}")
        password = self.get_password(f"{Fore.GREEN}Mot de passe: {Style.RESET_ALL}")
        
        passwords = self.load_passwords()
        passwords[platform] = {
            "password": password,
            "date": datetime.now().isoformat()
        }
        self.save_passwords(passwords)
        self.print_centered(f"Mot de passe pour {platform} ajouté avec succès.", Fore.GREEN)
        self.get_user_input(f"{Fore.CYAN}Appuyez sur Entrée pour continuer...{Style.RESET_ALL}")

    def generate_password(self):
        self.print_menu("Générer un mot de passe aléatoire", [])
        length = int(self.get_user_input(f"{Fore.GREEN}Longueur du mot de passe (8-32): {Style.RESET_ALL}"))
        length = max(8, min(length, 32))
        password = ''.join(secrets.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=') for _ in range(length))
        self.print_centered(f"Mot de passe généré: {password}", Fore.YELLOW)
        
        save = self.get_user_input(f"{Fore.GREEN}Voulez-vous sauvegarder ce mot de passe? (o/n): {Style.RESET_ALL}").lower()
        if save == 'o':
            platform = self.get_user_input(f"{Fore.GREEN}Nom de la plateforme: {Style.RESET_ALL}")
            passwords = self.load_passwords()
            passwords[platform] = {
                "password": password,
                "date": datetime.now().isoformat()
            }
            self.save_passwords(passwords)
            self.print_centered(f"Mot de passe pour {platform} sauvegardé avec succès.", Fore.GREEN)
        self.get_user_input(f"{Fore.CYAN}Appuyez sur Entrée pour continuer...{Style.RESET_ALL}")

    def view_password(self):
        self.print_menu("Voir un mot de passe", [])
        self.list_platforms()
        print("\n")
        platform = self.get_user_input(f"{Fore.GREEN}Entrez le nom de la plateforme (ou 'q' pour quitter): {Style.RESET_ALL}")
        if platform.lower() == 'q':
            return

        passwords = self.load_passwords()
        if platform in passwords:
            self.print_centered(f"Plateforme: {platform}", Fore.YELLOW)
            self.print_centered(f"Mot de passe: {passwords[platform]['password']}", Fore.YELLOW)
            self.print_centered(f"Date d'ajout: {passwords[platform]['date']}", Fore.YELLOW)
        
            date_added = datetime.fromisoformat(passwords[platform]['date'])
            if datetime.now() - date_added > timedelta(days=180):
                self.print_centered("ATTENTION: Ce mot de passe a plus de 6 mois.", Fore.RED)
                update = self.get_user_input(f"{Fore.GREEN}Voulez-vous le mettre à jour? (o/n): {Style.RESET_ALL}").lower()
                if update == 'o':
                    self.update_password(platform)
        else:
            self.print_centered("Plateforme non trouvée.", Fore.RED)
        self.get_user_input(f"{Fore.CYAN}Appuyez sur Entrée pour continuer...{Style.RESET_ALL}")

    def update_password(self, platform=None):
        self.print_menu("Mettre à jour un mot de passe", [])
        if platform is None:
            platform = self.get_user_input(f"{Fore.GREEN}Nom de la plateforme à mettre à jour: {Style.RESET_ALL}")
        
        passwords = self.load_passwords()
        if platform in passwords:
            new_password = self.get_password(f"{Fore.GREEN}Nouveau mot de passe: {Style.RESET_ALL}")
            passwords[platform] = {
                "password": new_password,
                "date": datetime.now().isoformat()
            }
            self.save_passwords(passwords)
            self.print_centered(f"Mot de passe pour {platform} mis à jour avec succès.", Fore.GREEN)
        else:
            self.print_centered("Plateforme non trouvée.", Fore.RED)
        self.get_user_input(f"{Fore.CYAN}Appuyez sur Entrée pour continuer...{Style.RESET_ALL}")

    def change_master_password(self):
        self.print_menu("Changer le mot de passe maître", [])
        current_password = self.get_password(f"{Fore.GREEN}Entrez votre mot de passe maître actuel: {Style.RESET_ALL}")
        with open(self.master_file, 'r') as f:
            master_data = json.load(f)
        
        salt = base64.b64decode(master_data['salt'])
        stored_verifier = base64.b64decode(master_data['verifier'])
        
        if hashlib.sha256(self.derive_key(current_password, salt)).digest() != stored_verifier:
            self.print_centered("Mot de passe maître incorrect.", Fore.RED)
            self.get_user_input(f"{Fore.CYAN}Appuyez sur Entrée pour continuer...{Style.RESET_ALL}")
            return
        
        new_password = self.get_password(f"{Fore.GREEN}Nouveau mot de passe maître: {Style.RESET_ALL}")
        confirm_password = self.get_password(f"{Fore.GREEN}Confirmez le nouveau mot de passe maître: {Style.RESET_ALL}")
        
        if new_password != confirm_password:
            self.print_centered("Les mots de passe ne correspondent pas.", Fore.RED)
            self.get_user_input(f"{Fore.CYAN}Appuyez sur Entrée pour continuer...{Style.RESET_ALL}")
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
        self.print_centered("Mot de passe maître changé avec succès.", Fore.GREEN)
        self.get_user_input(f"{Fore.CYAN}Appuyez sur Entrée pour continuer...{Style.RESET_ALL}")

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
            self.print_centered("Aucune plateforme enregistrée.", Fore.YELLOW)
        else:
            self.print_centered("Plateformes enregistrées :", Fore.CYAN)
            for platform, data in passwords.items():
                date_added = datetime.fromisoformat(data['date'])
                days_old = (datetime.now() - date_added).days
                self.print_centered(f"- {platform} (ajouté il y a {days_old} jours)", Fore.GREEN)
                if days_old > 180:
                    self.print_centered("  ATTENTION: Ce mot de passe a plus de 6 mois.", Fore.RED)
        self.print_centered(f"\nTotal: {len(passwords)} plateforme(s)", Fore.YELLOW)

    def delete_password(self):
        self.print_menu("Supprimer un mot de passe", [])
        self.list_platforms()
        print("\n")
        platform = self.get_user_input(f"{Fore.GREEN}Entrez le nom de la plateforme à supprimer (ou 'q' pour quitter): {Style.RESET_ALL}")
        if platform.lower() == 'q':
            return

        passwords = self.load_passwords()
        if platform in passwords:
            confirm = self.get_user_input(f"{Fore.YELLOW}Êtes-vous sûr de vouloir supprimer le mot de passe pour {platform}? (o/n): {Style.RESET_ALL}").lower()
            if confirm == 'o':
                del passwords[platform]
                self.save_passwords(passwords)
                self.print_centered(f"Mot de passe pour {platform} supprimé avec succès.", Fore.GREEN)
            else:
                self.print_centered("Suppression annulée.", Fore.YELLOW)
        else:
            self.print_centered("Plateforme non trouvée.", Fore.RED)
        self.get_user_input(f"{Fore.CYAN}Appuyez sur Entrée pour continuer...{Style.RESET_ALL}")

    def run(self):
        self.initialize()
        self.show_animation()
        
        if not self.login():
            self.print_centered("Échec de l'authentification. Au revoir!", Fore.RED)
            return
        
        while True:
            options = [
                "Ajouter un mot de passe",
                "Générer un mot de passe aléatoire",
                "Voir un mot de passe",
                "Mettre à jour un mot de passe",
                "Supprimer un mot de passe",
                "Changer le mot de passe maître",
                "Quitter"
            ]
            self.print_menu("Menu Principal", options)
            choice = self.get_user_choice(len(options))
            
            if choice == 1:
                self.add_password()
            elif choice == 2:
                self.generate_password()
            elif choice == 3:
                self.view_password()
            elif choice == 4:
                self.update_password()
            elif choice == 5:
                self.delete_password()
            elif choice == 6:
                self.change_master_password()
            elif choice == 7:
                self.clear_screen()
                self.print_centered("Merci d'avoir utilisé le gestionnaire de mots de passe. Au revoir!", Fore.YELLOW)
                break

def get_usb_path():
    if platform.system() == "Windows":
        drive = input("Entrez la lettre du lecteur USB (ex: D): ")
        return f"{drive}:\\"
    elif platform.system() == "Linux":
        return input("Entrez le point de montage USB (ex: /media/username/USB_NAME): ")
    elif platform.system() == "Darwin":  # macOS
        return input("Entrez le chemin de la clé USB (ex: /Volumes/USB_NAME): ")
    else:
        raise NotImplementedError("Système d'exploitation non supporté")

if __name__ == "__main__":
    usb_path = get_usb_path()
    
    if not os.path.exists(usb_path):
        print(Fore.RED + "Chemin USB non valide. Veuillez vérifier votre clé USB." + Style.RESET_ALL)
    else:
        pm = PasswordManager(usb_path)
        pm.run()