"""
MIT License

Copyright (c) 2019 NinjaSnail1080

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from ..utils import ans_to_id, get_region, raise_connection_error
from ..exceptions import CantGoBackAnyFurther
import aiohttp
import re
import time
import json

# * URLs for the API requests
NEW_SESSION_URL = "https://{}/ws/new_session?callback=jQuery331005089254861332693_{}&partner=1&player=website-desktop&uid_ext_session={}&frontaddr={}&constraint=ETAT%%3C%%3E%%27AV%%27&constraint=ETAT<>'AV'"
ANSWER_URL = "https://{}/ws/answer?callback=jQuery331005089254861332693_{}&session={}&signature={}&step={}&answer={}"
BACK_URL = "https://{}/ws/cancel_answer?callback=jQuery331005089254861332693_{}&session={}&signature={}&step={}&answer=-1"
WIN_URL = "https://{}/ws/list?callback=jQuery331005089254861332693_{}&session={}&signature={}&step={}"


class Akinator():
    """A class that represents an Akinator game [ASYNC VERSION].

    The first thing you want to do after calling an instance of this class is to call "Akinator.start_game()".
    """
    __slots__ = ("server", "session", "signature", "uid", "frontaddr", "timestamp",
                 "question", "progression", "step", "name", "description", "picture")

    def __init__(self):
        self.server = None
        self.session = None
        self.signature = None
        self.uid = None
        self.frontaddr = None
        self.timestamp = None

        self.question = None
        self.progression = None
        self.step = None

    def _update(self, resp, start=False):
        """Update class variables"""

        if start:
            self.session = int(resp["parameters"]["identification"]["session"])
            self.signature = int(
                resp["parameters"]["identification"]["signature"])
            self.question = str(
                resp["parameters"]["step_information"]["question"])
            self.progression = float(
                resp["parameters"]["step_information"]["progression"])
            self.step = int(resp["parameters"]["step_information"]["step"])
        else:
            self.question = str(resp["parameters"]["question"])
            self.progression = float(resp["parameters"]["progression"])
            self.step = int(resp["parameters"]["step"])

    def _parse_response(self, response):
        """Parse the JSON response and turn it into a Python object"""

        return json.loads(",".join(response.split("(")[1::])[:-1])

    async def _get_session_info(self):
        """Get uid and frontaddr from akinator.com/game"""

        info_regex = re.compile(
            "var uid_ext_session = '(.*)'\\;\\n.*var frontaddr = '(.*)'\\;")

        async with aiohttp.ClientSession() as session:
            async with session.get("https://en.akinator.com/game") as w:
                match = info_regex.search(await w.text())

        self.uid, self.frontaddr = match.groups()[0], match.groups()[1]

    async def start_game(self, language=None):
        """(coroutine)
        Start an Akinator game. Run this function first before the others. Returns a string containing the first question

        The "language" parameter can be left as None for English, the default language, or it can be set to one of the following (case-insensitive):
            - "en": English (default)
            - "en2": Second English server. Use if the main one is down
            - "en3": Third English server. Use if the other two are down
            - "en_animals": English server for guessing animals
            - "en_objects": English server for guessing objects
            - "ar": Arabic
            - "cn": Chinese
            - "de": German
            - "de_animals": German server for guessing animals
            - "es": Spanish
            - "es2": Second Spanish server. Use if the main one is down
            - "es_animals": Spanish server for guessing animals
            - "fr": French
            - "fr2": Second French server. Use if the main one is down
            - "fr_animals": French server for guessing animals
            - "fr_objects": French server for guessing objects
            - "il": Hebrew
            - "it": Italian
            - "it_animals": Italian server for guessing animals
            - "jp": Japanese
            - "jp_animals": Japanese server for guessing animals
            - "kr": Korean
            - "nl": Dutch
            - "pl": Polish
            - "pt": Portuguese
            - "ru": Russian
            - "tr": Turkish
        You can also put the name of the language spelled out, like "spanish", "korean", "french_animals", etc.
        """
        self.timestamp = time.time()
        self.server = get_region(language)
        await self._get_session_info()

        async with aiohttp.ClientSession() as session:
            async with session.get(NEW_SESSION_URL.format(self.server, self.timestamp, self.uid, self.frontaddr)) as w:
                resp = self._parse_response(await w.text())

        if resp["completion"] == "OK":
            self._update(resp, True)
            return self.question
        else:
            return raise_connection_error(resp["completion"])

    async def answer(self, ans):
        """(coroutine)
        Answer the current question, which you can find with "Akinator.question". Returns a string containing the next question

        The "ans" parameter must be one of these:
            - "yes" OR "y" OR "0" for YES
            - "no" OR "n" OR "1" for NO
            - "i" OR "idk" OR "i dont know" OR "i don't know" OR "2" for I DON'T KNOW
            - "probably" OR "p" OR "3" for PROBABLY
            - "probably not" OR "pn" OR "4" for PROBABLY NOT
        """
        ans = ans_to_id(ans)

        async with aiohttp.ClientSession() as session:
            async with session.get(ANSWER_URL.format(self.server, self.timestamp, self.session, self.signature, self.step, ans)) as w:
                resp = self._parse_response(await w.text())

        if resp["completion"] == "OK":
            self._update(resp)
            return self.question
        else:
            return raise_connection_error(resp["completion"])

    async def back(self):
        """(coroutine)
        Goes back to the previous question. Returns a string containing that question

        If you're on the first question and you try to go back again, the CantGoBackAnyFurther exception will be raised
        """
        if self.step == 0:
            raise CantGoBackAnyFurther(
                "You were on the first question and couldn't go back any further")

        async with aiohttp.ClientSession() as session:
            async with session.get(BACK_URL.format(self.server, self.timestamp, self.session, self.signature, self.step)) as w:
                resp = self._parse_response(await w.text())

        if resp["completion"] == "OK":
            self._update(resp)
            return self.question
        else:
            return raise_connection_error(resp["completion"])

    async def win(self):
        """(coroutine)
        Get Aki's guesses for who the person you're thinking of is based on your answers to the questions.

        This function returns a list of dictionaries containing 4 variables:
            - name: The name of the person Aki guessed
            - description: A short description of that person
            - picture: A direct link to an image of the person
            - progression: The probability that this is the correct person

        It's recommended that you call this function when Aki's progression is above 80%. You can get his current progression via "Akinator.progression"
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(WIN_URL.format(self.server, self.timestamp, self.session, self.signature, self.step)) as w:
                resp = self._parse_response(await w.text())

        if resp["completion"] == "OK":
            guesses = []
            for guess in resp["parameters"]["elements"]:
                guess = guess["element"]
                guess_dict = {
                    'name': guess['name'],
                    'description': guess['description'],
                    'picture': guess["absolute_picture_path"],
                    'probability': float(guess['proba']) * 100
                }
                guesses.append(guess_dict)

            return guesses
        else:
            return raise_connection_error(resp["completion"])
