import random

class Mastermind:
    def __init__(self, couleurs, taille, maxessais):
        self.couleurs = couleurs
        self.taille = taille
        self.maxessais = maxessais
        self.codesecret = self.generercode()
        self.essais = []

    def generercode(self):
        return [random.choice(self.couleurs) for _ in range(self.taille)]

    def ajoutessai(self, essai):
        self.essais.append(essai)

    def verifessai(self, essai):
        bon = 0
        mauvais = 0
        code = self.codesecret.copy()
        essai = essai.copy()
        for i in range(self.taille):
            if essai[i] == code[i]:
                bon += 1
                code[i] = None
                essai[i] = "_"
        for i in range(self.taille):
            if essai[i] in code and essai[i] != "_":
                mauvais += 1
                code[code.index(essai[i])] = None
        return bon, mauvais

    def affres(self, bon, mauvais):
        print(f"Correct : {bon} | Partiel : {mauvais}  (trop fort ou pas ?)")

class Joueur:
    def __init__(self, nom):
        self.nom = nom

    def proposercode(self, taille, couleurs):
        code = input(f"{self.nom}, balance ton code de {taille} couleurs : ").upper()
        while len(code) != taille or any(c not in couleurs for c in code):
            print("Nope, c'est pas bon, recommence !")
            code = input(f"{self.nom}, balance ton code de {taille} couleurs : ").upper()
        return list(code)

class Partie:
    def __init__(self, joueur, mastermind):
        self.joueur = joueur
        self.mastermind = mastermind

    def lancer(self):
        print("Let's go ! On démarre la partie !")
        print("Couleurs dispo : " + " ".join(self.mastermind.couleurs))
        print(f"Trouve le code de {self.mastermind.taille} couleurs, t'as {self.mastermind.maxessais} essais.")
        while len(self.mastermind.essais) < self.mastermind.maxessais:
            essai = self.joueur.proposercode(self.mastermind.taille, self.mastermind.couleurs)
            self.mastermind.ajoutessai(essai)
            bon, mauvais = self.mastermind.verifessai(essai)
            self.mastermind.affres(bon, mauvais)
            if bon == self.mastermind.taille:
                print(f"GG {self.joueur.nom}, t'as cracké le code en {len(self.mastermind.essais)} essais !")
                return
        print(f"Aïe, t'as perdu... Le code c'était : {''.join(self.mastermind.codesecret)}")