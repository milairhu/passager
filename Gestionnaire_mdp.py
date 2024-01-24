"""
Générateur de mots de passe :

L'utilisateur rentre l'URL du site sur lequel il veut créer un mot de passe ou retrouver son mot de passe.

    -   si le mot de passe pour ce site existe déjà : l'affiche à l'utilisateur
    -   sinon : crée un mot de passe et l'affiche

Les mots de passe sont stockés dans un fichier au format json.
Possibilités d'amélioration : utiliser une clé pour encoder et décoder les mots de passe sur le fichier json ou le fichier.

"""
import base64
import os
from tkinter import *

from cryptography.fernet import Fernet
import json

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

"""
data = json.load(mon_fichier) : lire

json.dump(monDico, monFichier) : ecrire
"""

encrypted_file_name = "psw.json"

# Génère une clé pour le chiffrement
def generate_key():
    return Fernet.generate_key()


# Chiffre les données avec la clé
def encrypt_data(key, data):
    cipher = Fernet(key)
    encrypted_data = cipher.encrypt(data.encode())
    return encrypted_data


# Déchiffre les données avec la clé
def decrypt_data(key, encrypted_data):
    cipher = Fernet(key)
    decrypted_data = cipher.decrypt(encrypted_data).decode()
    return decrypted_data


# Calcule le hash du psw entré par l'utilisateur
def get_key(psw):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b'salt',
        iterations=390000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(psw.encode('utf-8')))
    return key


def handle_psw():
    key = get_key(varPsw.get())
    site = ligneEdit.get().lower()

    with open(encrypted_file_name, 'rb') as file:
        encrypted_data = file.read()

    try:
        # Déchiffre les données
        decrypted_data = decrypt_data(key, encrypted_data)
    except:
        # Si l'utilisateur a rentré un mauvais mdp
        return

    # Charger les données JSON décryptées
    data = json.loads(decrypted_data)

    existe = data.get(site, "nil")

    if existe != "nil":
        # le lien entré a déjà un mot de passe associé
        str = data[site]
        varOut1.set('Mot de passe existant : ')
        varOut2.set(str)

    elif site != "":  # il faut générer un mdp

        """
        Un bon mot de passe doit contenir au moins 12 caractères et 4 types différents : 
            des minuscules, des majuscules, des chiffres et des caractères spéciaux.
        (source : www.cnil.fr)
        """
        import string
        import secrets

        # Génération du mdp grâce aux librairies spécialisées
        str = ""
        maj, minus, chiffre, speciaux = False, False, False, False
        voc = string.ascii_letters + string.digits + "!*?#%_$&/<>"

        while not (len(str) >= 12 and (maj and minus and chiffre and speciaux)):
            car = secrets.choice(voc)  # Choix d'un
            str += car

            if car.islower():
                minus = True
            elif car.isupper():
                maj = True
            elif car.isdigit():
                chiffre = True
            else:
                speciaux = True

        # Il faut enregistrer dans fichier :
        nvElt = {}
        nvElt[site] = str

        data.update(nvElt)  # ajoute l'élément au json

        varOut1.set("Création d'un mot de passe " + " : ")
        varOut2.set(str)
        encrypted_data = encrypt_data(key, json.dumps(data))
        with open(encrypted_file_name, 'wb') as encrypted_file:
            encrypted_file.write(encrypted_data)


def get_user_psw():
    print("Fenêtre mdp\n")
    #Get user password
    entered_password = password_entry.get()

    if entered_password == "":
        return
    else : 
        print("Mot de passe : " + entered_password + "\n")
        key = get_key(entered_password)
        # Vérifiez le mot de passe (remplacez ceci par votre propre logique)
        if not os.path.exists(encrypted_file_name):
            # Si les fichiers n'existent pas
            # Crée fichier json
            new_empty_data = {}
            s = json.dumps(new_empty_data)
            encrypted_data = encrypt_data(key, s)
            with open(encrypted_file_name, "wb") as file:
                file.write(encrypted_data)

        with open(encrypted_file_name, 'rb') as file:
            encrypted_data = file.read()
        
        goodPsw = False
        try:
            # Déchiffre les données, renvoie une erreur si la clé n'est pas la bonne
            decrypt_data(key, encrypted_data)
            goodPsw = True
            # Mot de passe correct, affichez l'input pour les liens URL
            display_main_frame()
        except Exception as e:
            if not goodPsw:
                print(e)
                # Mot de passe incorrect, affichez un message d'erreur
                error_message.pack()
        

def display_main_frame():
    
    #### Suppression des éléments pour saisie du mot de passe
    password_label.pack_forget()
    password_entry.pack_forget()
    password_button.pack_forget()
    error_message.pack_forget()

    ## Affichage des nouveaux éléments
    
    inp.pack(side=TOP, anchor=CENTER, pady=10)
    out.pack(side=TOP)
    bouton.pack(side=TOP, anchor=CENTER)

def on_ok_button_click():
    # Suppression des éléments de la page d'accueil
    welcome_title.pack_forget()
    info_label.pack_forget()
    ok_button.pack_forget()

    # Affichage des éléments pour saisie du mot de passe
    password_label.pack()
    password_entry.pack()
    password_button.pack()

if __name__ == '__main__':

    main_frame = Tk()
    main_frame.title("Gestionnaire de mots de passe")
    main_frame.resizable(height=FALSE, width=FALSE)
    #main_frame.geometry("450x150")

    # Page d'accueil
    welcome_title = Frame(main_frame)
    welcome_title = Label(main_frame, text="Bienvenue!", font=("Helvetica", 24, "bold"))

    info_label = Frame(main_frame)
    info_label = Label(main_frame, text="Vous allez devoir entrer le mot de passe que vous utiliserez pour avoir accès à l'application. \nAttention, il doit être robuste et rester secret!")

    ok_button = Frame(main_frame)
    ok_button = Button(main_frame, text="Ok!", command=on_ok_button_click)

    ## Entrée du mot de passe

    #### Message d'erreur en cas de mot de passe incorrect
    error_message = Frame(main_frame)
    error_message = Label(main_frame, text="Mot de passe incorrect. Réessayez.", fg="red")

    #### Pour saisie du mot de passe
    varPsw = StringVar()
    password_label = Frame(main_frame)
    password_label = Label(main_frame, text="Entrez votre mot de passe:")

    password_entry = Frame(main_frame)
    password_entry = Entry(main_frame, show="*", textvariable=varPsw)

    password_button = Frame(main_frame)
    password_button = Button(main_frame, text="Se connecter", command=get_user_psw)

    ## Fenêtre principale

    #### Ligne d'entrée URL

    inp = Frame(main_frame)

    labelIn = Label(inp, text="Entrez l'URL du site : ")
    labelIn.pack(side=LEFT)
    varLigne = StringVar()
    ligneEdit = Entry(inp, width=50, textvariable=varLigne)
    ligneEdit.pack(side=RIGHT)

    #### Label de sortie URL

    out = Frame(main_frame)
    varOut1 = StringVar()
    varOut1.set("Lancez pour afficher le mot de passe : ")
    labelOut = Label(out, textvariable=varOut1, pady=15)
    labelOut.pack(side=LEFT)
    varOut2 = StringVar()
    lineOut = Entry(out, textvariable=varOut2)
    lineOut.pack(side=RIGHT)

    #### Bouton validation URL
    bouton = Frame(main_frame)
    bouton = Button(main_frame, text="Générer / Chercher le mdp", padx=50, pady=10, command=handle_psw)

    
    # On vérifie si psw.json existe déjà, si non, on afffiche la page d'accueil
    if not os.path.exists(encrypted_file_name):
        welcome_title.pack(side=TOP, anchor=CENTER, pady=10)
        info_label.pack(side=TOP)
        ok_button.pack(side=TOP, anchor=CENTER, pady=10)
    else:
        # Affichage des éléments pour saisie du mot de passe
        password_label.pack()
        password_entry.pack()
        password_button.pack()

    
    main_frame.mainloop()
