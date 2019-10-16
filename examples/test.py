"""A simple test of the Akinator class"""

import akinator

aki = akinator.Akinator()

try:
    q = aki.start_game()
except akinator.AkiConnectionFailure:
    try:
        q = aki.start_game("en2")
    except akinator.AkiConnectionFailure:
        q = aki.start_game("en3")

while aki.progression <= 80:
    a = input(q + "\n\t")
    if a == "b":
        try:
            q = aki.back()
        except akinator.CantGoBackAnyFurther:
            pass
    else:
        q = aki.answer(a)
aki.win()

correct = input(f"It's {aki.name} ({aki.description})! Was I correct?\n{aki.picture}\n\t")
if correct.lower() == "yes" or correct.lower() == "y":
    print("Yay\n")
else:
    print("Oof\n")
