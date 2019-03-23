"""A simple test of the async Akinator class"""

from akinator.async_aki import Akinator
import akinator
import asyncio

aki = Akinator()


async def main():
    q = await aki.start_game()
    while aki.progression <= 85:
        a = input(q + "\n\t")
        if a == "b":
            try:
                q = await aki.back()
            except akinator.CantGoBackAnyFurther:
                pass
        else:
            q = await aki.answer(a)
    await aki.win()
    correct = input(f"It's {aki.name} ({aki.description})! Was I correct?\n{aki.picture}\n\t")
    if correct.lower() == "yes" or correct.lower() == "y":
        print("Yay\n")
    else:
        print("Oof\n")

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
