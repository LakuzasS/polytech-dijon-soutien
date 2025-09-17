import random
import os
import json
class Stats:
    def __init__(self, path=None):
        if path is None:
            self.dossier = os.path.dirname(__file__)
        elif os.path.isdir(path):
            self.dossier = path
        else:
            self.dossier = os.path.dirname(path) or '.'
        self.fnb = f"{self.dossier}/.mm_nb_parties"
        self.fsc = f"{self.dossier}/.mm_score_total"

    def nettoiepseudo(self, pseudo):
        if not pseudo:
            return None
        s = ''.join(c for c in pseudo if c.isalnum() or c == '_')
        return s or None

    def chemins(self, pseudo):
        sp = self.nettoiepseudo(pseudo)
        if not sp:
            return self.fnb, self.fsc
        return f"{self.dossier}/.mm_{sp}_nb_parties", f"{self.dossier}/.mm_{sp}_score_total"

    def lire(self, pseudo=None):
        nb = 0
        sc = 0
        fnb, fsc = self.chemins(pseudo)
        try:
            if os.path.exists(fnb):
                with open(fnb, 'r') as f:
                    nb = int(f.read().strip() or 0)
        except Exception:
            nb = 0
        try:
            if os.path.exists(fsc):
                with open(fsc, 'r') as f:
                    sc = int(f.read().strip() or 0)
        except Exception:
            sc = 0
        return {'nb_parties': nb, 'score_total': sc}

    def ajout(self, score, pseudo=None):
        s = self.lire(pseudo)
        nb = s.get('nb_parties', 0) + 1
        sc = s.get('score_total', 0) + int(score)
        fnb, fsc = self.chemins(pseudo)
        try:
            with open(fnb, 'w') as f:
                f.write(str(nb))
        except Exception:
            pass
        try:
            with open(fsc, 'w') as f:
                f.write(str(sc))
        except Exception:
            pass
        return {'nb_parties': nb, 'score_total': sc}

    def remet(self, pseudo=None):
        fnb, fsc = self.chemins(pseudo)
        try:
            with open(fnb, 'w') as f:
                f.write('0')
        except Exception:
            pass
        try:
            with open(fsc, 'w') as f:
                f.write('0')
        except Exception:
            pass
        return {'nb_parties': 0, 'score_total': 0}
 

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
        stats = STATS.lire(self.joueur.nom)
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
                nstats = STATS.ajout(score, self.joueur.nom)
                print(f"Nouvelles stats -> parties: {nstats['nb_parties']} | score total: {nstats['score_total']}")
                return
        print(f"Aïe, t'as perdu... Le code c'était : {''.join(self.mastermind.codesecret)}")
        score = 0
        nstats = STATS.ajout(score, self.joueur.nom)
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
    STATS.remet()
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