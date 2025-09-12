import json
import random

class Joueur:
	def __init__(self, nom, jetons=0, ia=None):
		self.nom = nom
		self.jetons = jetons
		self.cartes = []
		self.mise = 0
		self.ia = ia 
		self.stats = {'victoires': 0, 'defaites': 0, 'egalites': 0}
	
	def action_ia(self, main, banque_carte):
		t = sum(main)
		as_nb = main.count(1)
		while as_nb > 0 and t + 10 <= 21:
			t += 10
			as_nb -= 1
		if self.ia == 'prudent':
			return '2' if t >= 15 else '1'
		if self.ia == 'tete':
			return '2' if t >= 18 else '1'
		if self.ia == 'calcul':
			if t >= 17:
				return '2'
			if banque_carte >= 7 and t < 17:
				return '1'
			if banque_carte <= 6 and t < 12:
				return '1'
			return '2'
		return None
	
	def split(self):
		return len(self.cartes) == 2 and self.cartes[0] == self.cartes[1]
	
	def __init__(self, nom, jetons=0):
		self.nom = nom
		self.jetons = jetons
		self.cartes = []
		self.mise = 0
		
	def main(self):
		self.cartes = [self.tirer_carte(), self.tirer_carte()]
		
	def tirer_carte(self):
		return random.randint(1, 11)
	
	def pioche(self):
		self.cartes.append(self.tirer_carte())
		
	def total(self):
		t = sum(self.cartes)
		as_nb = self.cartes.count(1)
		while as_nb > 0 and t + 10 <= 21:
			t += 10
			as_nb -= 1
		return t
	
	def affiche(self, cache=False):
		if cache:
			print(self.nom, ": [", self.cartes[0], ", ?]")
		else:
			print(self.nom, ":", self.cartes, "(total:", self.total(), ")")

def regles():
	print("Le but est d'approcher 21 sans le dépasser. Les figures valent 10, l'As vaut 1 ou 11. La banque tire jusqu'à 17. Possibilités : tirer, s'arrêter, doubler (double la mise, une carte), se coucher (récupère la moitié de la mise).")

import os

class Blackjack:
	def charger_stats(self):
		try:
			with open('stats.json', 'r') as f:
				return json.load(f)
		except:
			return {}
		
	def sauvegarder_stats(self, stats):
		with open('stats.json', 'w') as f:
			json.dump(stats, f)

	def __init__(self):
		self.fichier = "argent.txt"
		self.mise_min = 10
		self.mise_max = 100

	def charger_jetons(self):
		if os.path.exists(self.fichier):
			try:
				with open(self.fichier, "r") as f:
					return int(f.read())
			except:
				return 100
		return 100
	
	def sauvegarder_jetons(self, jetons):
		with open(self.fichier, "w") as f:
			f.write(str(jetons))

	def menu(self):
		while True:
			print("1. Jouer\n2. Règles\n3. Stats\n4. Quitter")
			c = input("> ")
			if c == "1":
				self.partie()
			elif c == "2":
				regles()
			elif c == "3":
				stats = self.charger_stats()
				if not stats:
					print("Aucune stat, go jouer!")
				else:
					for nom, s in stats.items():
						print(f"{nom} : {s['victoires']} win / {s['defaites']} lose / {s['egalites']} égalités")
			elif c == "4":
				break

	def partie(self):
		nb = 0
		while nb < 1 or nb > 6:
			try:
				nb = int(input("Combien de joueurs ? (1-6): "))
			except:
				pass
		joueurs = []
		for i in range(nb):
			nom = input(f"Pseudo du joueur {i+1} : ")
			ia = None
			if nom.lower() in ['prudent', 'tete', 'calcul']:
				ia = nom.lower()
				nom = nom.capitalize()
			jetons = self.charger_jetons() if i == 0 else 100
			joueurs.append(Joueur(nom, jetons, ia))
		mise_max = self.mise_max
		while any(j.jetons >= self.mise_min for j in joueurs):
			print("\n--- Nouvelle manche ---")
			for j in joueurs:
				if j.jetons < self.mise_min:
					print(f"{j.nom} t'es fauché, next round!")
					continue
				print(f"{j.nom} : {j.jetons} jetons | Mise min: {self.mise_min} max: {mise_max}")
				while True:
					try:
						mise = int(input(f"{j.nom}, ta mise ? "))
						if self.mise_min <= mise <= min(mise_max, j.jetons):
							break
					except:
						pass
				j.mise = mise
				j.jetons -= mise
			b = Joueur("Banque")
			for j in joueurs:
				j.main()
			b.main()
			for j in joueurs:
				j.affiche()
			b.affiche(cache=True)
			assurance = [0]*nb
			assurance_prise = [False]*nb
			for idx, j in enumerate(joueurs):
				if b.cartes[0] == 1 and j.jetons >= (j.mise + (j.mise + 1) // 2):
					rep = input(f"{j.nom}, banque a un As. Assurance ? (o/n): ")
					if rep.lower() == "o":
						assurance[idx] = (j.mise + 1) // 2
						j.jetons -= assurance[idx]
						assurance_prise[idx] = True
			victoire = [False]*nb
			couche = [False]*nb
			for idx, j in enumerate(joueurs):
				if j.jetons < 0: continue
				mains = [j.cartes]
				mises = [j.mise]
				split_fait = False
				if j.split() and j.jetons >= j.mise:
					rep = 'n'
					if j.ia is None:
						rep = input(f"{j.nom}, tu veux split ? (o/n): ")
					elif j.ia == 'tete':
						rep = 'o' if j.cartes[0] in [8,11] else 'n'
					elif j.ia == 'prudent':
						rep = 'o' if j.cartes[0] == 8 else 'n'
					elif j.ia == 'calcul':
						rep = 'o' if j.cartes[0] in [8,9,11] else 'n'
					if rep.lower() == "o":
						split_fait = True
						j.jetons -= j.mise
						mains = [[j.cartes[0], j.tirer_carte()], [j.cartes[1], j.tirer_carte()]]
						mises = [j.mise, j.mise]
				for m_idx, main in enumerate(mains):
					fini = False
					while not fini:
						t = sum(main)
						as_nb = main.count(1)
						while as_nb > 0 and t + 10 <= 21:
							t += 10
							as_nb -= 1
						if t >= 21:
							break
						print(f"{j.nom} main {m_idx+1 if split_fait else ''} : {main} (total: {t})")
						print("1. Tirer 2. Stop 3. Doubler 4. Coucher")
						if j.ia:
							c = j.action_ia(main, b.cartes[0])
							print(f"({j.nom} IA choisit {c})")
						else:
							c = input(f"{j.nom} > ")
						if c == "1":
							main.append(j.tirer_carte())
						elif c == "2":
							fini = True
						elif c == "3" and j.jetons >= mises[m_idx]:
							j.jetons -= mises[m_idx]
							mises[m_idx] *= 2
							main.append(j.tirer_carte())
							fini = True
						elif c == "4":
							couche[idx] = True
							fini = True
					if m_idx == 0:
						j.cartes = main
					else:
						joueurs.append(Joueur(j.nom+f"_split", j.jetons, j.ia))
						joueurs[-1].cartes = main
						joueurs[-1].mise = mises[m_idx]
			print("\nBanque time!")
			b.affiche()
			while b.total() < 17:
				b.pioche()
				b.affiche()
			blackjack_banque = (b.total() == 21 and len(b.cartes) == 2)
			stats = self.charger_stats()
			for idx, j in enumerate(joueurs):
				if j.jetons < 0: continue
				blackjack_joueur = (j.total() == 21 and len(j.cartes) == 2)
				if couche[idx]:
					j.jetons += j.mise // 2
					print(f"{j.nom} s'est couché, récupère {j.mise//2} jetons. Next!")
					j.stats['defaites'] += 1
					continue
				if assurance_prise[idx]:
					if blackjack_banque:
						print(f"{j.nom} : la banque a blackjack, assurance payée!")
						j.jetons += 2 * assurance[idx]
						if not blackjack_joueur:
							print(f"{j.nom} a perdu sa mise!")
							j.stats['defaites'] += 1
						else:
							print(f"{j.nom} égalité, récupère sa mise!")
							j.jetons += j.mise
							j.stats['egalites'] += 1
						continue
					else:
						print(f"{j.nom} : la banque n'a pas blackjack, assurance perdue!")
				gain = 0
				if j.total() > 21:
					print(f"{j.nom} a explosé, next!")
					j.stats['defaites'] += 1
				elif blackjack_joueur and not blackjack_banque:
					gain = int(j.mise * 2.5)
					print(f"{j.nom} BLACKJACK ! +{gain} jetons, la classe.")
					j.jetons += gain
					victoire[idx] = True
					j.stats['victoires'] += 1
				elif b.total() > 21:
					gain = 2 * j.mise
					print(f"{j.nom} win! +{gain} jetons, t'es riche!")
					j.jetons += gain
					victoire[idx] = True
					j.stats['victoires'] += 1
				elif blackjack_banque and not blackjack_joueur:
					print(f"{j.nom} perd, la banque a blackjack!")
					j.stats['defaites'] += 1
				elif j.total() > b.total():
					gain = 2 * j.mise
					print(f"{j.nom} win! +{gain} jetons, t'es chaud!")
					j.jetons += gain
					victoire[idx] = True
					j.stats['victoires'] += 1
				elif j.total() == b.total():
					print(f"{j.nom} égalité, récupère {j.mise} jetons.")
					j.jetons += j.mise
					j.stats['egalites'] += 1
				else:
					print(f"{j.nom} perd, la banque est trop forte!")
					j.stats['defaites'] += 1
				stats[j.nom] = j.stats
			if victoire.count(True) > 0:
				mise_max *= 2
			for i, j in enumerate(joueurs):
				if i == 0:
					self.sauvegarder_jetons(j.jetons)
			self.sauvegarder_stats(stats)
			if victoire.count(True) > 0:
				mise_max *= 2
			for i, j in enumerate(joueurs):
				if i == 0:
					self.sauvegarder_jetons(j.jetons)
			if all(j.jetons < self.mise_min for j in joueurs):
				print("Plus personne n'a de jetons, c'est la dèche!")
				break
			r = input("On refait une manche ? (o/n): ")
			if r.lower() != "o":
				break

if __name__ == "__main__":
	Blackjack().menu()
