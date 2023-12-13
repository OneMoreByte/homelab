#!/usr/bin/env python3

import random

def get_name():
    pokemon = []
    with open("./resources/pokemon.csv") as handle:
        for line in handle:
            poke = line.split(",")
            pokemon.append(poke)
    selected = random.choice(pokemon)
    with open("./resources/pokemon.csv", "w") as handle:
        for p in pokemon:
            if p == selected:
                p[-1] = "used\n"
            handle.write(",".join(p))
    return selected[1].lower()


if __name__ == "__main__":
    print(f'"{get_name()}"')
