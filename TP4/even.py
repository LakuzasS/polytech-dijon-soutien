from random import randint

for i in range(15):
    x = randint(0, 100)
    print(x)
    if x % 2 :
        print("Impair !")
    else:
        print("Pair !")