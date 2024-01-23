"""
Générateur de mots de passe :

L'utilisateur rentre l'URL du site sur lequel il veut créer un mot de passe ou retrouver son mot de passe.

    -   si le mot de passe pour ce site existe déjà : l'affiche à l'utilisateur
    -   sinon : crée un mot de passe et l'affiche

Les mots de passe sont stockés dans un fichier au format json.
Possibilités d'amélioration : utiliser une clé pour encoder et décoder les mots de passe sur le fichier json ou le fichier.

"""
import os
from tkinter import *
from cryptography.fernet import Fernet

import json
"""
data = json.load(mon_fichier) : lire

json.dump(monDico, monFichier) : ecrire
"""
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


def handle_psw():
    site = ligneEdit.get().lower()

    encrypted_file_name = "psw.json"
    key_file_name = "encryption_key.key"

    if not os.path.exists(encrypted_file_name):
        # Si les fichiers n'existent pas
        # Crée fichier clé
        key = generate_key()
        with open(key_file_name, 'wb') as key_file:
            key_file.write(key)
        # Crée fichier json
        new_empty_data = {}
        s = json.dumps(new_empty_data)
        encrypted_data = encrypt_data(key, s)
        with open(encrypted_file_name, "wb") as file:
            file.write(encrypted_data)

    # Ouvre les fichiers
    with open(key_file_name, 'rb') as key_file:
        key = key_file.read()

    with open(encrypted_file_name, 'rb') as file:
        encrypted_data = file.read()

    # Déchiffre les données
    decrypted_data = decrypt_data(key, encrypted_data)

    # Charger les données JSON décryptées
    data = json.loads(decrypted_data)

    existe = data.get(site, "nil")

    if existe != "nil":
        #le lien entré a déjà un mot de passe associé
        str=data[site]
        varOut1.set('Mot de passe existant : ')
        varOut2.set(str)

    elif site!="":  # il faut générer un mdp

        """
        Un bon mot de passe doit contenir au moins 12 caractères et 4 types différents : 
            des minuscules, des majuscules, des chiffres et des caractères spéciaux.
        (source : www.cnil.fr)
        """
        import string
        import secrets

        #Génération du mdp grâce aux librairies spécialisées
        str = ""
        maj, minus, chiffre, speciaux = False, False, False, False
        voc = string.ascii_letters + string.digits + "!*?#%_$&/<>"

        while not (len(str) >= 12 and (maj and minus and chiffre and speciaux)):
            car = secrets.choice(voc) #Choix d'un
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

        varOut1.set("Création d'un mot de passe "+" : ")
        varOut2.set(str)
        encrypted_data = encrypt_data(key, json.dumps(data))
        with open(encrypted_file_name, 'wb') as encrypted_file:
            encrypted_file.write(encrypted_data)

if __name__ == '__main__':

    # Affichage

    main_frame=Tk()
    main_frame.title("Gestionnaire de mots de passe")
    main_frame.resizable(height=FALSE, width=FALSE)
    main_frame.geometry("450x150")


    #### Ligne d'entrée

    inp = Frame(main_frame)

    labelIn = Label(inp,text="Entrez l'URL du site : ")
    labelIn.pack(side=LEFT)
    varLigne= StringVar()
    ligneEdit = Entry(inp, width=50, textvariable=varLigne)
    ligneEdit.pack(side=RIGHT)
    inp.pack(side=TOP, anchor=CENTER, pady=10)

    #### Label de sortie
    out = Frame(main_frame)
    varOut1=StringVar()
    varOut1.set("Lancez pour afficher le mot de passe : ")
    labelOut = Label(out,textvariable=varOut1,pady=15)
    labelOut.pack(side=LEFT)
    varOut2 = StringVar()
    lineOut = Entry(out, textvariable=varOut2 )
    lineOut.pack(side=RIGHT)
    out.pack(side=TOP)

    #### Bouton validation

    bouton = Button(main_frame, text="Générer / Chercher le mdp", padx=50, pady=10, command=handle_psw)
    bouton.pack(side=TOP, anchor=CENTER)

    main_frame.mainloop()








