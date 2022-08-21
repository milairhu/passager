"""
Générateur de mots de passe :

L'utilisateur rentre l'URL du site sur lequel il veut créer un mot de passe ou retrouver son mot de passe.

    -   si le mot de passe pour ce site existe déjà : l'affiche à l'utilisateur
    -   sinon : crée un mot de passe et l'affiche

Les mots de passe sont stockés dans un fichier au format json.
Possibilités d'amélioration : utiliser une clé pour encoder et décoder les mots de passe sur le fichier json ou le fichier.

"""

from tkinter import *

import json
"""
data = json.load(mon_fichier) : lire

json.dump(monDico, monFichier) : ecrire
"""


def handle_psw():

    site = ligneEdit.get().lower()

    try:
        fichier = open("psw.json", "r+")


    except:
        fichier = open("psw.json", "w")
        fichier.write("{\n}")
        fichier.close()
        fichier = open("psw.json", "r+")

    data = json.load(fichier)

    existe = data.get(site, "nil")

    if existe != "nil":  # ok
        #il faut décoder le code du fichier
        str=data[site]
        posElt = 0
        for elt in data.keys():
            if elt==site:
                break
            else :
                posElt+=1

        #A COMPLETER : réécrire chaque lettre avec grâce à clé inversée
        #res=""
        #for c in str:
        #    res+=c-12*posElt-5


        varOut1.set('Mot de passe existant : ')
        varOut2.set(str)

    else:  # il faut générer un mdp

        """
        Un bon mot de passe doit contenir au moins 12 caractères et 4 types différents : 
            des minuscules, des majuscules, des chiffres et des caractères spéciaux.
        (source : www.cnil.fr)
        """
        import string
        import secrets

        str = ""
        maj, minus, chiffre, speciaux = False, False, False, False
        voc = string.ascii_letters + string.digits + "!*?#%_$&/<>"

        while not (len(str) >= 12 and (maj and minus and chiffre and speciaux)):
            car = secrets.choice(voc)
            str += car

            if car.islower():
                minus = True
            elif car.isupper():
                maj = True
            elif car.isdigit():
                chiffre = True
            else:
                speciaux = True

        #On encode l'élément suivant une clé spécifique à chaque élément
        #code=""
        #for c in str:
        #    code+= (c+12*(len(data)+5))%len(voc)  # len(data) réfère à la position que elt va occuper dans dictionnaire

        # Il faut enregistrer dans fichier :
        nvElt = {}
        nvElt[site] = str

        data.update(nvElt)  # ajoute l'élément
        #print(data)

        varOut1.set("Création d'un mot de passe "+" : ")
        varOut2.set(str)
        fichier.seek(0)
        json.dump(data, fichier)  # modifie fichier en mettant en JSON

    fichier.close()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

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









