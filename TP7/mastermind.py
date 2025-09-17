import random
import os
import itertools
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


def valider_opts(opts):
    cols = normaliser_couleurs(opts.get('couleurs', []))
    if not cols:
        return False, 'Liste de couleurs invalide'
    taille = opts.get('taille', 4)
    try:
        taille = int(taille)
    except Exception:
        return False, 'Taille invalide'
    if taille < 1:
        return False, 'Taille doit etre >=1'
    maxe = opts.get('maxessais', 12)
    try:
        maxe = int(maxe)
    except Exception:
        return False, 'Max essais invalide'
    if maxe < 1:
        return False, 'Max essais doit etre >=1'
    return True, ''

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

class Ordi:
    def deviner(self, couleurs, taille, maxessais, secret):
        poss = [list(p) for p in itertools.product(couleurs, repeat=taille)]
        essais = 0
        while essais < maxessais and poss:
            ess = list(random.choice(poss))
            essais += 1
            print(f"Ordi essai {essais} : {''.join(ess)}")
            bon, mal = calcrep(secret, ess)
            if bon == taille:
                print(f"GG l'ordi a trouve en {essais} essais")
                return essais
            poss = [p for p in poss if calcrep(p, ess) == (bon, mal)]
        print("L'ordi n'a pas reussi a trouver le code")
        return None

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
    print("5) Mode inverse (l'ordi devine)")
    print("6) Jouer (GUI)")


def show_stats(_pseudo=None):
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


def modeinverse():
    print("Mode inverse : duel humain vs ordi")
    couleurs = DEFAULTS['couleurs']
    taille = DEFAULTS['taille']
    maxessais = DEFAULTS['maxessais']

    print("\nPhase 1 - Tu dois deviner un code aleatoire")
    m_h = Mastermind(couleurs, taille, maxessais)
    j = Joueur()
    p = Partie(j, m_h)
    score_humain = p.lancer()
    print(f"Score humain: {score_humain}")

    print("\nPhase 2 - Choisis un code pour que l'ordi l'essaie")
    code = input(f"Donne ton code secret de {taille} lettres: ").strip().upper()
    while len(code) != taille or any(c not in couleurs for c in code):
        print("Code invalide, recommence")
        code = input(f"Donne ton code secret de {taille} lettres: ").strip().upper()
    secret = list(code)
    o = Ordi()
    essais = o.deviner(couleurs, taille, maxessais, secret)
    if essais:
        score_ordi = max(0, maxessais - essais)
        print(f"Score ordi: {score_ordi}")
        STATS.ajout(score_ordi)
    else:
        score_ordi = 0
        print("Score ordi: 0")
        STATS.ajout(0)

    # Score final combiné
    final = int(score_humain) - int(score_ordi)
    print(f"\nScore final (humain - ordi) = {score_humain} - {score_ordi} = {final}")
    STATS.ajout(final)
    show_stats()


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
    ok, msg = valider_opts(opts)
    if not ok:
        print('Config invalide :', msg)
        print('Je garde les valeurs par defaut.')
        return
    DEFAULTS.update(opts)
    print('Nouvelles options en place :', DEFAULTS)


def play_gui():
    try:
        import pygame
    except Exception:
        print("pygame n'est pas disponible. Installez pygame pour utiliser la GUI.")
        return
    pygame.init()
    size = (600, 300)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Mastermind - GUI minimal')
    font = pygame.font.SysFont(None, 24)
    couleurs = DEFAULTS['couleurs']
    taille = DEFAULTS['taille']
    maxessais = DEFAULTS['maxessais']
    mm = Mastermind(couleurs, taille, maxessais)
    entry = ''
    feedback = ''
    attempts = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    entry = entry[:-1]
                elif event.key == pygame.K_RETURN:
                    if len(entry) == taille and all(c in couleurs for c in entry):
                        guess = list(entry.upper())
                        attempts += 1
                        bon, mal = mm.verifessai(guess)
                        feedback = f"Correct : {bon} | Partiel : {mal}"
                        if bon == taille or attempts >= maxessais:
                            score = max(0, maxessais - attempts) if bon == taille else 0
                            STATS.ajout(score)
                            print(f"(GUI) Score: {score}")
                            running = False
                        entry = ''
                    else:
                        feedback = 'Entrée invalide'
                else:
                    ch = event.unicode.upper()
                    if ch.isalpha() and ch in couleurs and len(entry) < taille:
                        entry += ch
        screen.fill((20, 20, 20))
        screen.blit(font.render('Couleurs: ' + ' '.join(couleurs), True, (230,230,230)), (10,10))
        screen.blit(font.render('Saisie: ' + entry, True, (230,230,230)), (10,40))
        screen.blit(font.render('Feedback: ' + feedback, True, (230,230,230)), (10,70))
        screen.blit(font.render(f'Essais: {attempts}/{maxessais}', True, (230,230,230)), (10,100))
        pygame.display.flip()
        pygame.time.Clock().tick(30)
    pygame.quit()


def main():
    show_stats()
    while True:
        affichermenu()
        choix = input("Ton choix > ").strip()
        if choix == '1':
            lancerjeu()
        elif choix == '5':
            modeinverse()
        elif choix == '6':
            play_gui()
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