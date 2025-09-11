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

class Blackjack:
	def __init__(self):
		pass
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
		j = Joueur("Joueur", 100)
		while j.jetons > 0:
			print("Jetons:", j.jetons)
			while True:
				try:
					mise = int(input("Mise: "))
					if 1 <= mise <= j.jetons:
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
				continue
			if j.total() > 21:
				print("Perdu")
			else:
				print("Banque joue")
				b.affiche()
				while b.total() < 17:
					b.pioche()
					b.affiche()
				if b.total() > 21 or j.total() > b.total():
					print("Gagné +", j.mise, "jetons")
					j.jetons += 2 * j.mise
				elif j.total() == b.total():
					print("Egalité +", j.mise, "jetons")
					j.jetons += j.mise
				else:
					print("Perdu")
			if j.jetons == 0:
				print("Plus de jetons.")
				break
			r = input("Rejouer ? (y/n): ")
			if r.lower() != "y":
				break

if __name__ == "__main__":
	Blackjack().menu()
