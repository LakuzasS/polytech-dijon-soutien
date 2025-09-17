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