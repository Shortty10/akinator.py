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


class InvalidAnswerError(Exception):
    """Raised when the user inputs an invalid answer"""
    pass


class InvalidLanguageError(Exception):
    """Raised when the user inputs an invalid language"""
    pass


class AkiConnectionFailure(Exception):
    """Raised if the Akinator API fails to connect for some reason. Base class for AkiTimedOut, AkiNoQuestions, and AkiFailedToConnect"""


class AkiTimedOut(AkiConnectionFailure):
    """Raised if the Akinator session times out. Derived from AkiConnectionFailure"""
    pass


class AkiNoQuestions(AkiConnectionFailure):
    """Raised if the Akinator API runs out of questions to ask. This will happen once "Akinator.step" reaches 80. Derived from AkiConnectionFailure"""
    pass


class AkiFailedToConnect(AkiConnectionFailure):
    """Raised when the Akinator API failed to connect for some reason other than timing out or running out of questions. Derived from AkiConnectionFailure"""
    pass


class CantGoBackAnyFurther(Exception):
    """Raised when the user is on the first question and tries to go back further"""
    pass
