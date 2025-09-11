saisieInvalide = True
while saisieInvalide:
    try:
        x = int(input("Saisissez un entier : "))
        saisieInvalide = False
        print(f'Nombre saisi : {x}.')
    except:
        print("Saisie invalide")
        saisieInvalide = True
