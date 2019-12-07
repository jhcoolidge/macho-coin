from random import randint


def random_greeting():
    random_number = randint(1, 5)

    if random_number == 1:
        print("MACHOCOIN! FOR MACHO PEOPLE!")

    elif random_number == 2:
        print("In this world, only the MACHOEST SURVIVE!")

    elif random_number == 3:
        print("MACHOCOIN IS SOMETIMES TOO MACHO!\nSOMETIMES IT EVEN FLEXES ON OTHER CURRENCY!")

    elif random_number == 4:
        print("MACHOCOIN! For when your muscles are too big!")

    elif random_number == 5:
        print("MUSCLES\n" +
              "AND\n" +
              "COMPUTER\n" +
              "HAXX\n" +
              "OH YEAH!")

    return
