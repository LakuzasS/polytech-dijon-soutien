import random

class Joueur:
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
			print("1. Jouer\n2. Règles\n3. Quitter")
			c = input("> ")
			if c == "1":
				self.partie()
			elif c == "2":
				regles()
			elif c == "3":
				break
	def partie(self):
		j = Joueur("Joueur", self.charger_jetons())
		mise_max = self.mise_max
		while j.jetons > 0:
			print("Jetons:", j.jetons)
			print("Mise min:", self.mise_min, "Mise max:", mise_max)
			while True:
				try:
					mise = int(input("Mise: "))
					if self.mise_min <= mise <= min(mise_max, j.jetons):
						break
				except:
					pass
			j.mise = mise
			j.jetons -= mise
			b = Joueur("Banque")
			j.main()
			b.main()
			j.affiche()
			b.affiche(cache=True)
			double = False
			couche = False
			victoire = False
			assurance = 0
			assurance_prise = False
			if b.cartes[0] == 1 and j.jetons >= (j.mise + (j.mise + 1) // 2):
				rep = input("Banque a un As. Prendre assurance ? (o/n): ")
				if rep.lower() == "o":
					assurance = (j.mise + 1) // 2
					j.jetons -= assurance
					assurance_prise = True
			while True:
				if j.total() >= 21:
					break
				print("1. Tirer 2. S'arrêter 3. Doubler 4. Se coucher")
				c = input("> ")
				if c == "1":
					j.pioche()
					j.affiche()
				elif c == "2":
					break
				elif c == "3" and j.jetons >= j.mise:
					j.jetons -= j.mise
					j.mise *= 2
					j.pioche()
					j.affiche()
					double = True
					break
				elif c == "4":
					couche = True
					break
			if couche:
				j.jetons += j.mise // 2
				print("Couché. +", j.mise // 2, "jetons.")
				self.sauvegarder_jetons(j.jetons)
				continue
			if j.total() > 21:
				print("Perdu")
			else:
				print("Banque joue")
				b.affiche()
				while b.total() < 17:
					b.pioche()
					b.affiche()
				blackjack_banque = (b.total() == 21 and len(b.cartes) == 2)
				blackjack_joueur = (j.total() == 21 and len(j.cartes) == 2)
				if assurance_prise:
					if blackjack_banque:
						print("Banque a blackjack. Assurance payée.")
						j.jetons += 2 * assurance
						if not blackjack_joueur:
							print("Perdu")
						else:
							print("Egalité +", j.mise, "jetons")
							j.jetons += j.mise
						self.sauvegarder_jetons(j.jetons)
						continue
					else:
						print("Banque n'a pas blackjack. Assurance perdue.")
				if b.total() > 21 or j.total() > b.total():
					print("Gagné +", j.mise, "jetons")
					j.jetons += 2 * j.mise
					victoire = True
				elif j.total() == b.total():
					print("Egalité +", j.mise, "jetons")
					j.jetons += j.mise
				else:
					print("Perdu")
			if victoire:
				mise_max *= 2
			self.sauvegarder_jetons(j.jetons)
			if j.jetons == 0:
				print("Plus de jetons.")
				break
			r = input("Rejouer ? (y/n): ")
			if r.lower() != "y":
				break

if __name__ == "__main__":
	Blackjack().menu()
