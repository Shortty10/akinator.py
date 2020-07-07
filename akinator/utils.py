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

from .exceptions import InvalidAnswerError, InvalidLanguageError, AkiConnectionFailure, AkiTimedOut, AkiNoQuestions, AkiServerDown, AkiTechnicalError


def ans_to_id(ans):
    """Convert an input answer string into an Answer ID for Akinator"""

    ans = str(ans).lower()
    if ans == "yes" or ans == "y" or ans == "0":
        return "0"
    elif ans == "no" or ans == "n" or ans == "1":
        return "1"
    elif ans == "i" or ans == "idk" or ans == "i dont know" or ans == "i don't know" or ans == "2":
        return "2"
    elif ans == "probably" or ans == "p" or ans == "3":
        return "3"
    elif ans == "probably not" or ans == "pn" or ans == "4":
        return "4"
    else:
        raise InvalidAnswerError("""
        You put "{}", which is an invalid answer.
        The answer must be one of these:
            - "yes" OR "y" OR "0" for YES
            - "no" OR "n" OR "1" for NO
            - "i" OR "idk" OR "i dont know" OR "i don't know" OR "2" for I DON'T KNOW
            - "probably" OR "p" OR "3" for PROBABLY
            - "probably not" OR "pn" OR "4" for PROBABLY NOT
        """.format(ans))


def get_region(lang=None):
    """Returns an Aki URI and server based on what language is input"""

    if lang:
        lang = lang.lower().replace(" ", "")
        if lang.endswith(("animal", "object")):
            lang += "s"

    if lang is None or lang == "en" or lang == "english":
        return {"uri": "en.akinator.com",
                "server": "srv13.akinator.com:9361"}
    elif lang == "en_animals" or lang == "english_animals":
        return {"uri": "en.akinator.com",
                "server": "srv2.akinator.com:9318"}
    elif lang == "en_objects" or lang == "english_objects":
        return {"uri": "en.akinator.com",
                "server": "srv2.akinator.com:9319"}
    elif lang == "ar" or lang == "arabic":
        return {"uri": "ar.akinator.com",
                "server": "srv2.akinator.com:9315"}
    elif lang == "cn" or lang == "chinese":
        return {"uri": "cn.akinator.com",
                "server": "srv11.akinator.com:9344"}
    elif lang == "de" or lang == "german":
        return {"uri": "de.akinator.com",
                "server": "srv14.akinator.com:9369"}
    elif lang == "de_animals" or lang == "german_animals":
        return {"uri": "de.akinator.com",
                "server": "srv14.akinator.com:9370"}
    elif lang == "es" or lang == "spanish":
        return {"uri": "es.akinator.com",
                "server": "srv6.akinator.com:9354"}
    elif lang == "es_animals" or lang == "spanish_animals":
        return {"uri": "es.akinator.com",
                "server": "srv13.akinator.com:9362"}
    elif lang == "fr" or lang == "french":
        return {"uri": "fr.akinator.com",
                "server": "srv3.akinator.com:9331"}
    elif lang == "fr_animals" or lang == "french_animals":
        return {"uri": "fr.akinator.com",
                "server": "srv3.akinator.com:9329"}
    elif lang == "fr_objects" or lang == "french_objects":
        return {"uri": "fr.akinator.com",
                "server": "srv3.akinator.com:9330"}
    elif lang == "il" or lang == "hebrew":
        return {"uri": "il.akinator.com",
                "server": "srv12.akinator.com:9339"}
    elif lang == "it" or lang == "italian":
        return {"uri": "it.akinator.com",
                "server": "srv9.akinator.com:9380"}
    elif lang == "it_animals" or lang == "italian_animals":
        return {"uri": "it.akinator.com",
                "server": "srv9.akinator.com:9383"}
    elif lang == "jp" or lang == "japanese":
        return {"uri": "jp.akinator.com",
                "server": "srv11.akinator.com:9349"}
    elif lang == "jp_animals" or lang == "japanese_animals":
        return {"uri": "jp.akinator.com",
                "server": "srv11.akinator.com:9352"}
    elif lang == "kr" or lang == "korean":
        return {"uri": "kr.akinator.com",
                "server": "srv2.akinator.com:9316"}
    elif lang == "nl" or lang == "dutch":
        return {"uri": "nl.akinator.com",
                "server": "srv9.akinator.com:9381"}
    elif lang == "pl" or lang == "polish":
        return {"uri": "pl.akinator.com",
                "server": "srv14.akinator.com:9143"}
    elif lang == "pt" or lang == "portuguese":
        return {"uri": "pt.akinator.com",
                "server": "srv11.akinator.com:9350"}
    elif lang == "ru" or lang == "russian":
        return {"uri": "ru.akinator.com",
                "server": "srv12.akinator.com:9340"}
    elif lang == "tr" or lang == "turkish":
        return {"uri": "tr.akinator.com",
                "server": "srv3.akinator.com:9332"}
    else:
        raise InvalidLanguageError("You put \"{}\", which is an invalid language.".format(lang))


def raise_connection_error(response):
    """Raise the proper error if the API failed to connect"""

    if response == "KO - SERVER DOWN":
        raise AkiServerDown("Akinator's servers are down in this region. Try again later or use a different language")
    elif response == "KO - TECHNICAL ERROR":
        raise AkiTechnicalError("Akinator's servers have had a technical error. Try again later or use a different language")
    elif response == "KO - TIMEOUT":
        raise AkiTimedOut("Your Akinator session has timed out")
    elif response == "KO - ELEM LIST IS EMPTY" or response == "WARN - NO QUESTION":
        raise AkiNoQuestions("\"Akinator.step\" reached 80. No more questions")
    else:
        raise AkiConnectionFailure("An unknown error has occured. Server response: {}".format(response))
