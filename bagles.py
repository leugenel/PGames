from random import shuffle
from unittest.mock import Mock, patch, PropertyMock, MagicMock
from unittest import TestCase
from argparse import ArgumentParser

class Bagles:

    GUESSES = 10
    NUMBER_OF_DIGITS = 3

    def __init__(self, n_guesses: int = GUESSES, silent : bool = False) -> None:
        self.silent = silent
        self.n_guesses = n_guesses
        first_digits = [i for i in range(1,10)]
        shuffle(first_digits)
        self.__hidden_number = "".join(str(c) for c in first_digits[:self.NUMBER_OF_DIGITS])
    
    @property
    def hidden_number(self):
        return self.__hidden_number

    def bagles(self) -> bool:
        print(f"DEBUG: {self.hidden_number}")

        for i in range(self.n_guesses):
            user_input = self.get_user_input(i)
            if not user_input:
                continue
            if user_input == self.hidden_number:
                print("Great you won! This is a number!") if not self.silent else None
                return True
            res = self.guess(user_input)
            self.print_round_res(res) if not self.silent else None
        
        print(f"The number was {self.hidden_number}") if not self.silent else None
        return False
    
    def print_round_res(self, res: dict):
        if res.get("Bagles", False):
            print("Bagles")
            return
        for _ in range(res.get("Fermi", 0)):
            print("Fermi")
        for _ in range(res.get("Pico", 0)):
            print("Pico")    

    def guess(self, user_input: str) -> dict:
        res = dict()
        res["Bagles"] = True
        for i in range(self.NUMBER_OF_DIGITS):
            if user_input[i] == self.hidden_number[i]:
                res["Fermi"] = 1 if not res.get("Fermi") else res["Fermi"] + 1 
                res["Bagles"] = False
                continue
            if user_input[i] in self.hidden_number:
                res["Pico"] = 1 if not res.get("Pico") else res["Pico"] + 1 
                res["Bagles"] = False  
                continue
        return res

    def get_user_input(self, counter: int = 0) -> str:
        user_input = input(f"Guess # {counter} ==>:")
        try:
            if 999 < int(user_input) or int(user_input) < 100 or len(list(set(user_input))) != self.NUMBER_OF_DIGITS:
                raise ValueError
        except ValueError:
            print("You should enter 3-digit number with the different digits")
            return None
        return user_input

class BaglesTest(TestCase):
    @patch('builtins.input', return_value='123')
    def test_bagles(self, input):
        bgl = Bagles()
        type(bgl).hidden_number = PropertyMock(return_value="123")
        assert bgl.bagles() == True
       
greeting = """
            I am thinking of a 3-digit number. Try to guess what it is.
            Here are some clues:
            When I say:
            Pico
            Fermi
            That means:
            One digit is correct but in the wrong position.
            One digit is correct and in the right position.
            No digit is correct.
            Bagels
            I have thought up a number.
            All digits should be different.
            You have 10 guesses to get it."""

def parse():
    parser = ArgumentParser()
    parser.add_argument('-n', dest='num_guesses', type=int, default=10, required=False)
    parser.add_argument('-s', dest='silent',  action='store_true', default=False)
    parser.add_argument('-t', dest='test', action='store_true', default=False)
    return parser.parse_args()

if __name__ == '__main__':
    args = parse()
    if not args.silent:
        print(greeting)
    Bagles(n_guesses=args.num_guesses, silent=args.silent).bagles() if not args.test else BaglesTest().test_bagles()
   