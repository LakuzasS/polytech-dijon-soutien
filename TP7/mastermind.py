import random
import os
import json

class Stats:
    def __init__(self, path=None):
        self.path = path or os.path.join(os.path.dirname(__file__), '.mm_stats')

    def lire(self):
        if not os.path.exists(self.path):
            return {'nb_parties': 0, 'score_total': 0}
        try:
            with open(self.path, 'r') as f:
                return json.load(f)
        except Exception:
            return {'nb_parties': 0, 'score_total': 0}

    def ajouter(self, score):
        s = self.lire()
        s['nb_parties'] = s.get('nb_parties', 0) + 1
        s['score_total'] = s.get('score_total', 0) + int(score)
        try:
            with open(self.path, 'w') as f:
                json.dump(s, f)
        except Exception:
            pass
        return s

    def reset(self):
        s = {'nb_parties': 0, 'score_total': 0}
        try:
            with open(self.path, 'w') as f:
                json.dump(s, f)
        except Exception:
            pass
        return s

STATS = Stats()

DEFAULTS = {
    'couleurs': ['R','G','B','Y','P','N'],
    'taille': 4,
    'maxessais': 12,
}

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
        stats = STATS.lire()
        nbp = stats.get('nb_parties', 0)
        tot = stats.get('score_total', 0)
        moy = (tot / nbp) if nbp else 0
        print(f"Stats -> parties: {nbp} | score total: {tot} | moyenne: {moy:.2f}")
        while len(self.mastermind.essais) < self.mastermind.maxessais:
            essai = self.joueur.proposercode(self.mastermind.taille, self.mastermind.couleurs)
            self.mastermind.ajoutessai(essai)
            bon, mauvais = self.mastermind.verifessai(essai)
            self.mastermind.affres(bon, mauvais)
            if bon == self.mastermind.taille:
                essais = len(self.mastermind.essais)
                score = max(0, self.mastermind.maxessais - essais)
                print(f"GG {self.joueur.nom}, t'as cracké le code en {essais} essais ! Score: {score}")
                nstats = STATS.ajouter(score)
                print(f"Nouvelles stats -> parties: {nstats['nb_parties']} | score total: {nstats['score_total']}")
                return
        print(f"Aïe, t'as perdu... Le code c'était : {''.join(self.mastermind.codesecret)}")
        score = 0
        nstats = STATS.ajouter(score)
        print(f"Nouvelles stats -> parties: {nstats['nb_parties']} | score total: {nstats['score_total']}")


def affichermenu():
    print("\n=== Mastermind ===")
    print("1) Jouer")
    print("2) Remettre a zero les stats")
    print("3) Quitter")
    print("4) Configurer les options du jeu")


def lancerjeu():
    print("Lancer une partie !")
    couleurs = DEFAULTS['couleurs']
    taille = DEFAULTS['taille']
    maxessais = DEFAULTS['maxessais']
    nom = input("Ton blaze ? ").strip() or "Toi"
    m = Mastermind(couleurs, taille, maxessais)
    j = Joueur(nom)
    p = Partie(j, m)
    p.lancer()


def remettrezero():
    STATS.reset()
    print("Ok, stats remises a zero. On repart a 0 !")


def configurer():
    print("Configurer les options du jeu :")
    cur = DEFAULTS.copy()
    print(f"Couleurs actuelles: {' '.join(cur['couleurs'])}")
    nc = input("Nouvelle liste de lettres pour couleurs (ex: RGBYPN) ou entree pour garder: ").upper().strip()
    if nc:
        cur['couleurs'] = list(nc)
    nt = input(f"Taille du code actuelle ({cur['taille']}) ou entree pour garder: ").strip()
    if nt:
        try:
            cur['taille'] = int(nt)
        except ValueError:
            print("Taille invalide, on garde la valeur precedente.")
    ne = input(f"Max essais actuelle ({cur['maxessais']}) ou entree pour garder: ").strip()
    if ne:
        try:
            cur['maxessais'] = int(ne)
        except ValueError:
            print("Max essais invalide, on garde la valeur precedente.")
    DEFAULTS.update(cur)
    print("Nouvelles options en place.")


def main():
    while True:
        affichermenu()
        choix = input("Ton choix > ").strip()
        if choix == '1':
            lancerjeu()
        elif choix == '4':
            configurer()
        elif choix == '2':
            remettrezero()
        elif choix == '3' or choix.lower() == 'q':
            print("A plus !")
            break
        else:
            print("Choix invalide, reessaie stp")


if __name__ == '__main__':
    main()