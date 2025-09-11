import random
import os

SCORE_FILE = "score.txt"

def difficulté():
    print("1 - Facile (1-100, 10 points)")
    print("2 - Moyen (1-1000, 30 points)")
    print("3 - Difficile (1-10000, 80 points)")
    while True:
        choix = input("Votre choix (1/2/3) : ")
        if choix == '1':
            return (1, 100, 10, "facile")
        elif choix == '2':
            return (1, 1000, 30, "moyen")
        elif choix == '3':
            return (1, 10000, 80, "difficile")
        else:
            print("Choix invalide.")

def score(pseudo, score, difficulte):
    try:
        with open(SCORE_FILE, "a") as f:
            f.write(f"{pseudo},{score},{difficulte}\n")
    except Exception as e:
        print("Erreur lors de la sauvegarde du score :", e)

def jouer():
    min, max, points, difficulte = difficulté()
    nombre = random.randint(min, max)
    win = False
    print(f"\nDeviner le nombre entre {min} et {max}. {points} points disponibles.")
    while points > 0 and not win:
        try:
            x = int(input(f"Saisir un entier entre {min} et {max} : "))
            if not (min <= x <= max):
                print(f"Saisie invalide. Entrer un nombre entre {min} et {max}.")
                continue
        except ValueError:
            print("Saisie invalide. Entrer un nombre entier.")
            continue

        if x < nombre:
            points -= 1
            print("Plus grand ! Points restants :", points)
        elif x > nombre:
            points -= 1
            print("Plus petit ! Points restants :", points)
        else:
            win = True
            print(f"Bravo, c'était {nombre}. {points} points restants.")

    if not win:
        print(f"Plus de points restant. Le nombre était {nombre}.")
    pseudo = input("Entrez votre pseudo pour enregistrer votre score : ")
    score(pseudo, points if win else 0, difficulte)

def print_scores():
    if not os.path.exists(SCORE_FILE):
        print("Aucun score enregistré.")
        return
    print("\n--- Scores enregistrés ---")
    with open(SCORE_FILE, "r") as f:
        for line in f:
            pseudo, score, diff = line.strip().split(",")
            print(f"{pseudo} | {score} points | difficulté : {diff}")
    print("-------------------------\n")

def menu():
    while True:
        print("\n--- Menu ---")
        print("1. Jouer")
        print("2. Afficher les scores")
        print("3. Quitter")
        choix = input()
        if choix == '1':
            jouer()
        elif choix == '2':
            print_scores()
        elif choix == '3':
            break
        else:
            print("Choix invalide.")

if __name__ == "__main__":
    menu()


