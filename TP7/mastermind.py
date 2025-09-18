import random
import os
class Stats:
    def __init__(self, path=None):
        self.dossier = os.path.dirname(__file__)
        self.fnb = os.path.join(self.dossier, '.mm_nb_parties')
        self.fsc = os.path.join(self.dossier, '.mm_score_total')

    def _read_int(self, path, default=0):
        try:
            if os.path.exists(path):
                with open(path, 'r') as f:
                    return int(f.read().strip() or default)
        except Exception:
            pass
        return default

    def _write_int(self, path, value):
        try:
            with open(path, 'w') as f:
                f.write(str(int(value)))
        except Exception:
            pass

    def lire(self):
        nb = self._read_int(self.fnb, 0)
        sc = self._read_int(self.fsc, 0)
        return {'nb_parties': nb, 'score_total': sc}

    def ajout(self, score):
        s = self.lire()
        nb = s.get('nb_parties', 0) + 1
        sc = s.get('score_total', 0) + int(score)
        self._write_int(self.fnb, nb)
        self._write_int(self.fsc, sc)
        return {'nb_parties': nb, 'score_total': sc}

    def remet(self):
        self._write_int(self.fnb, 0)
        self._write_int(self.fsc, 0)
        return {'nb_parties': 0, 'score_total': 0}
 
STATS = Stats()

DEFAULTS = {
    'couleurs': ['R','G','B','Y','P','N'],
    'taille': 4,
    'maxessais': 12,
}

def normaliser_couleurs(entree):
    if isinstance(entree, list):
        seq = ''.join(entree)
    else:
        seq = str(entree)
    seq = seq.upper().strip()
    seen = set()
    res = []
    for c in seq:
        if c.isalpha() and c not in seen:
            seen.add(c)
            res.append(c)
    return res

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
        return calcrep(self.codesecret, essai)

    def affres(self, bon, mauvais):
        print(f"Correct : {bon} | Partiel : {mauvais}")

def calcrep(secret, essai):
    bon = 0
    mal = 0
    code = secret.copy()
    tst = essai.copy()
    for i in range(len(secret)):
        if tst[i] == code[i]:
            bon += 1
            code[i] = None
            tst[i] = "_"
    for i in range(len(secret)):
        if tst[i] in code and tst[i] != "_":
            mal += 1
            code[code.index(tst[i])] = None
    return bon, mal

class Joueur:
    def __init__(self, nom=None):
        self.nom = nom

    def proposercode(self, taille, couleurs):
        code = input(f"Saisis le code de {taille} couleurs : ").upper()
        while len(code) != taille or any(c not in couleurs for c in code):
            print("Nope, c'est pas bon, recommence !")
            code = input(f"Saisis le code de {taille} couleurs : ").upper()
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
                print(f"GG, t'as cracké le code en {essais} essais ! Score: {score}")
                return score
        print(f"Aïe, t'as perdu... Le code c'était : {''.join(self.mastermind.codesecret)}")
        score = 0
        return score

def affichermenu():
    print("\n=== Mastermind ===")
    print("1) Jouer (terminal)")
    print("2) Remettre a zero les stats")
    print("3) Quitter")
    print("4) Configurer les options du jeu")

def show_stats():
    s = STATS.lire()
    nbp = s.get('nb_parties', 0)
    tot = s.get('score_total', 0)
    moy = (tot / nbp) if nbp else 0
    print(f"Stats (Global) -> parties: {nbp} | score total: {tot} | moyenne: {moy:.2f}")

def lancerjeu():
    print("Lancer une partie !")
    couleurs = DEFAULTS['couleurs']
    taille = DEFAULTS['taille']
    maxessais = DEFAULTS['maxessais']
    while True:
        m = Mastermind(couleurs, taille, maxessais)
        j = Joueur()
        p = Partie(j, m)
        score = p.lancer()
        nstats = STATS.ajout(score)
        print(f"Nouvelles stats -> parties: {nstats['nb_parties']} | score total: {nstats['score_total']}")
        print("\n=== Fin de la partie ===")
        show_stats()
        print("1) Rejouer")
        print("2) Remettre a zero les stats")
        print("3) Retour au menu principal")
        choix = input("Ton choix > ").strip()
        if choix == '1':
            continue
        elif choix == '2':
            remettrezero()
            print("Stats remises a zero.")
        else:
            break

def remettrezero():
    STATS.remet()
    print("Ok, stats remises a zero. On repart a 0 !")

def configurer():
    print("Config : laisse vide pour defaut (ex: RGBYPN)")
    c = input(f"Couleurs (suite de lettres, def {''.join(DEFAULTS['couleurs'])}): ")
    t = input(f"Taille code (def {DEFAULTS['taille']}): ")
    m = input(f"Max essais (def {DEFAULTS['maxessais']}): ")
    opts = {}
    opts['couleurs'] = normaliser_couleurs(c) if c else DEFAULTS['couleurs']
    try:
        opts['taille'] = int(t) if t else DEFAULTS['taille']
    except Exception:
        print('Taille invalide, jg garde la valeur precedente.')
        opts['taille'] = DEFAULTS['taille']
    try:
        opts['maxessais'] = int(m) if m else DEFAULTS['maxessais']
    except Exception:
        print('Max essais invalide, jg garde la valeur precedente.')
        opts['maxessais'] = DEFAULTS['maxessais']
    if not opts['couleurs'] or opts['taille'] < 1 or opts['maxessais'] < 1:
        print('Config invalide : valeurs incorrectes')
        print('Je garde les valeurs par defaut.')
        return
    DEFAULTS.update(opts)
    print('Nouvelles options en place :', DEFAULTS)


def main():
    show_stats()
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
