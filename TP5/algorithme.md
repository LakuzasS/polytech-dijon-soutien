# 🃏 Algorithme général du Blackjack 

## 🏠 Menu principal

- 🎮 Jouer une partie
- 📖 Règles du jeu
- 🚪 Quitter

---

## 🎲 Déroulement d'une partie

1. **Initialiser** le nombre de jetons du joueur
2. **Boucle de jeu** :
	 - Tant que le joueur veut continuer **et** a des jetons :
		 1. ▶️ **Démarrer une manche**
		 2. 🧾 Afficher le résultat et mettre à jour les jetons
		 3. 🔁 Proposer de rejouer ou quitter

---

## 🕹️ Fonction : Démarrer une manche

1. 💰 Demander la mise au joueur *(vérifier qu’il a assez de jetons)*
2. 🃏 Distribuer 2 cartes au joueur, 2 à la banque *(une cachée)*
3. 👀 Afficher la main du joueur et la première carte de la banque
4. 🔄 Tant que le joueur n’a pas arrêté/tiré trop :
	 - Proposer :
		 - 💤 Se coucher *(récupérer la moitié de la mise)*
		 - ✌️ Doubler *(double la mise, tire une carte)*
		 - ➕ Tirer une carte
		 - ✋ S’arrêter
	 - Gérer chaque choix *(mise à jour main/mise/jetons)*
5. 🏦 Révéler la main de la banque, tirer jusqu’à 17+
6. 🧮 Calculer le résultat *(voir fonction)*
7. 💵 Retourner le résultat et la mise gagnée/perdue

---

## 🧮 Fonction : Calculer la valeur d’une main

- Additionner les valeurs des cartes
- Gérer les As (1 ou 11 selon la main)

---

## 📖 Fonction : Afficher les règles

- Afficher les règles du blackjack