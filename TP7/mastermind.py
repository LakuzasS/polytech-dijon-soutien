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

    def jouer(self):
        print("Yo bienvenue sur le Mastermind :) Voici les couleurs dispo :")
        print(" ".join(self.couleurs))
        print(f"Faut trouver le code de {self.taille} couleurs, t'as {self.maxessais} essais. Vas-y, tente ta chance !")
        while len(self.essais) < self.maxessais:
            essai = input(f"Essai {len(self.essais)+1} : ").upper()
            if len(essai) != self.taille or any(c not in self.couleurs for c in essai):
                print("Rhoo, mets un code valide avec les bonnes couleurs !")
                continue
            essailist = list(essai)
            self.ajoutessai(essailist)
            bon, mauvais = self.verifessai(essailist)
            self.affres(bon, mauvais)
            if bon == self.taille:
                print(f"GG, t'as cracké le code en {len(self.essais)} essais !")
                return
        print(f"Aïe, t'as perdu... Le code c'était : {''.join(self.codesecret)}")

