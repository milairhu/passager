"""
Générateur et gestionnaire de mots de passe :

Deux fonctionnalités :

1) Génération : l'utilisateur rentre l'URL du site sur lequel il veut créer un mot de passe ou retrouver son mot de passe.

    -   si le mot de passe pour ce site existe déjà : l'affiche à l'utilisateur
    -   sinon : crée un mot de passe et l'affiche
2) Ajout manuel : de la même manière, l'utilisateur peut soit même modifier ou ajouter des mots de passes manuellement.
Les mots de passe sont stockés dans un fichier au format json, chiffré par son mot de passe principal.

"""
import base64
import os
from tkinter import *
from tkinter import ttk

from cryptography.fernet import Fernet
import json

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


encrypted_file_name = "psw"
max_attempt = 5

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

#Genere ou trouve le mdp pour un site donné
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
    existe = data["data"].get(site, "nil")

    if existe != "nil":
        # le lien entré a déjà un mot de passe associé
        str = data["data"][site]
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

        data["data"].update(nvElt)  # ajoute l'élément au json

        varOut1.set("Création d'un mot de passe " + " : ")
        varOut2.set(str)
        encrypted_data = encrypt_data(key, json.dumps(data))
        with open(encrypted_file_name, 'wb') as encrypted_file:
            encrypted_file.write(encrypted_data)

# Ajoute ou met à jour le mdp pour un site donné
def handle_man():
    key = get_key(varPsw.get())
    site = ligneEditMan.get().lower()
    psw = lineOutMan.get()

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

    existe = data["data"].get(site, "nil")

    if existe != "nil" and psw != "":
        # le lien entré a déjà un mot de passe associé
        str = data["data"][site]
        varOut1Man.set("Mise à jour de l'ancien mot de passe ( " + str + " ) : ")
        varOut2Man.set(psw)
        # Enregistrer dans fichier :
        nvElt = {}
        nvElt[site] = psw

        data["data"].update(nvElt)  # ajoute l'élément au json
        encrypted_data = encrypt_data(key, json.dumps(data))
        with open(encrypted_file_name, 'wb') as encrypted_file:
            encrypted_file.write(encrypted_data)

    elif site != "" and psw != "": 
        # on ajoute le mdp pour le nouveau site
        varOut1Man.set("Ajout d'un nouveau mot de passe : ")
        varOut2Man.set(psw)
        # Enregistrer dans fichier :
        nvElt = {}
        nvElt[site] = psw

        data["data"].update(nvElt)  # ajoute l'élément au json
        encrypted_data = encrypt_data(key, json.dumps(data))
        with open(encrypted_file_name, 'wb') as encrypted_file:
            encrypted_file.write(encrypted_data)


# Vérifie le mot de passe entré par l'utilisateur
def get_user_psw():
    #Get user password
    entered_password = password_entry.get()

    if entered_password == "":
        return
    else : 
        key = get_key(entered_password)
        # Vérifiez le mot de passe (remplacez ceci par votre propre logique)
        if not os.path.exists(encrypted_file_name):
            # Si le fichier n'existent pas
            # Crée fichier json
            new_empty_data = {}
            new_empty_data["data"] = {}
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
                # Mot de passe incorrect, affichez un message d'erreur
                error_message.grid(row=1, column=0, columnspan=2, pady=5)
                password_button.grid_forget()
                password_button.grid(row = 2, column = 0, columnspan=2, pady=10) 
        

def display_main_frame():
    
    #### Suppression des éléments pour saisie du mot de passe
    password_label.grid_forget()
    password_entry.grid_forget()
    password_button.grid_forget()
    error_message.grid_forget()

    ## Affichage des nouveaux éléments
    notebook.pack(fill='both', expand=True)
    inp.pack(side=TOP, anchor=CENTER, pady=10, padx=10)
    out.pack(side=TOP)
    bouton.pack(side=TOP, anchor=CENTER, pady=10)
    inpMan.pack(side=TOP, anchor=CENTER, pady=10, padx=10)
    outMan.pack(side=TOP)
    boutonMan.pack(side=TOP, anchor=CENTER, pady=10)

# Handle the click on the ok button on the welcome page
def on_ok_button_click():
    # Suppression des éléments de la page d'accueil
    welcome_title.pack_forget()
    info_label.pack_forget()
    ok_button.pack_forget()

    # Affichage des éléments pour saisie du mot de passe
    password_label.grid(row=0, column=0, padx=10, pady=10)
    password_entry.grid(row=0, column=1, padx=10, pady=10)
    password_button.grid(row = 1, column = 0, columnspan=2, pady=10) 

if __name__ == '__main__':

    main_frame = Tk()
    main_frame.title("Gestionnaire de mots de passe")
    main_frame.resizable(height=FALSE, width=FALSE)
    #main_frame.geometry("450x150")

    # Page d'accueil
    welcome_title = Frame(main_frame)
    welcome_title = Label(main_frame, text="Bienvenue!", font=("Helvetica", 24, "bold"))

    info_label = Frame(main_frame)
    info_label = Label(main_frame, text="Vous allez devoir entrer le mot de passe que vous utiliserez pour avoir accès à l'application. \nAttention, il doit être robuste et rester secret ! \nEt si vous l'oubliez, vous ne pourrez plus accéder à vos mots de passe.")

    ok_button = Frame(main_frame)
    ok_button = Button(main_frame, text="Ok !", command=on_ok_button_click)

    ## Entrée du mot de passe

    #### Message d'erreur en cas de mot de passe incorrect
    error_message = Frame(main_frame)
    error_message = Label(main_frame, text="Mot de passe incorrect. Réessayez.", fg="red")

    #### Pour saisie du mot de passe
    varPsw = StringVar()
    password_label = Frame(main_frame)
    password_label = Label(main_frame, text="Entrez votre mot de passe :")

    password_entry = Frame(main_frame)
    password_entry = Entry(main_frame, show="*", textvariable=varPsw)

    password_button = Frame(main_frame)
    password_button = Button(main_frame, text="Se connecter", command=get_user_psw)

    ## Fenêtre principale

    #### Création des onglets
    notebook = ttk.Notebook(main_frame)

    generation_frame = Frame(notebook)
    manual_frame = Frame(notebook)

    notebook.add(generation_frame, text="Génération / Gestion")
    notebook.add(manual_frame, text="Ajout Manuel / Mise à Jour ")

    #### Génération / Gestion

    ##### Ligne d'entrée génération

    inp = Frame(generation_frame)

    labelIn = Label(inp, text="Entrez l'URL du site : ")
    labelIn.pack(side=LEFT)
    varLigne = StringVar()
    ligneEdit = Entry(inp, width=50, textvariable=varLigne)
    ligneEdit.pack(side=RIGHT)

    ##### Label de sortie génération

    out = Frame(generation_frame)
    varOut1 = StringVar()
    varOut1.set("Lancez pour afficher le mot de passe : ")
    labelOut = Label(out, textvariable=varOut1, pady=15)
    labelOut.pack(side=LEFT)
    varOut2 = StringVar()
    lineOut = Entry(out, textvariable=varOut2)
    lineOut.pack(side=RIGHT)

    ##### Bouton validation génération
    bouton = Frame(generation_frame)
    bouton = Button(generation_frame, text="Générer / Chercher le mot de passe", padx=50, pady=10, command=handle_psw)

    #### Ajout Manuel / Mise à Jour

    ##### Ligne d'entrée de l'URL

    inpMan = Frame(manual_frame)

    labelInMan = Label(inpMan, text="Entrez l'URL du site : ")
    labelInMan.pack(side=LEFT)
    varURLMan = StringVar()
    ligneEditMan = Entry(inpMan, width=50, textvariable=varURLMan)
    ligneEditMan.pack(side=RIGHT)

    ##### Label de sortie URL

    outMan = Frame(manual_frame)
    varOut1Man = StringVar()
    varOut1Man.set("Entrez le mot de passe à enregistrer : ")
    labelOutMan = Label(outMan, textvariable=varOut1Man, pady=15)
    labelOutMan.pack(side=LEFT)
    varOut2Man = StringVar()
    lineOutMan = Entry(outMan, textvariable=varOut2Man)
    lineOutMan.pack(side=RIGHT)

    ##### Bouton validation génération
    boutonMan = Frame(manual_frame)
    boutonMan = Button(manual_frame, text="Créer / Mettre à jour le mot de passe", padx=50, pady=10, command=handle_man)
    
    
    # On vérifie si le fichier psw existe déjà, si non, on afffiche la page d'accueil
    if not os.path.exists(encrypted_file_name):
        welcome_title.pack(side=TOP, anchor=CENTER, pady=10)
        info_label.pack(side=TOP)
        ok_button.pack(side=TOP, anchor=CENTER, pady=10)
    else:
        # Affichage des éléments pour saisie du mot de passe
        
        password_label.grid(row=0, column=0, padx=10, pady=10)
        password_entry.grid(row=0, column=1, padx=10, pady=10)
        password_button.grid(row = 1, column = 0, columnspan=2, pady=10)
    
    main_frame.mainloop()
