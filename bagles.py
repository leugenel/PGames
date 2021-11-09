from random import shuffle
from unittest.mock import Mock, patch, PropertyMock, MagicMock
from unittest import TestCase
from argparse import ArgumentParser
from itertools import permutations

class Bagles:

    GUESSES = 10
    NUMBER_OF_DIGITS = 3

    def __init__(self, n_guesses: int = GUESSES, silent : bool = False, machine_input: bool = False) -> None:
        self.silent = silent
        self.n_guesses = n_guesses
        self.machine_input=machine_input
        self.__hidden_number = self.coin_number()
        self.machine_guess_number = "123"
        self.machine_numbers_for_choise = list(range(1,10))
        self.user_input = None
        self.guess_result = None
        self.number_permutations = list()
    
    @property
    def hidden_number(self):
        return self.__hidden_number

    def bagles(self) -> bool:
        print(f"DEBUG: {self.hidden_number}")

        for i in range(self.n_guesses):
            print(f"Guess #{i}")
            self.user_input = self.get_user_input(i)
            if not self.user_input:
                continue
            if self.user_input == self.hidden_number:
                print("Great you won! This is a number!") if not self.silent else None
                return True
            self.guess_result = self.guess(self.user_input)
            self.print_round_res(self.guess_result) if not self.silent else None
           
        print(f"The number was {self.hidden_number}") if not self.silent else None
        return False
    
    def machine_guess(self):
        if self.guess_result is not None and  self.guess_result.get("Pico", False) + self.guess_result.get("Fermi", False) == 3:
                print("Debug: 3 guess strategy")
                self.machine_guess_number = self.machine_3_good_answer_strategy()
        else:         
            if self.guess_result is not None and self.guess_result.get("Bagles", False):
                    self.machine_guess_bagles_answer_strategy()       
            self.machine_guess_number = self.coin_number(numbers=self.machine_numbers_for_choise)
        
        print(f"Machine guess: {self.machine_guess_number}")
        return self.machine_guess_number

    def machine_guess_bagles_answer_strategy(self):
        for i in self.machine_guess_number:
            self.machine_numbers_for_choise.remove(int(i))

    def machine_3_good_answer_strategy(self):
        digits_integer = tuple([int(i) for i in self.user_input]) # like (6, 7, 8)
        if len(self.number_permutations) == 0 : # only doing it first time, get all permutations of the number
            self.number_permutations = list(permutations(digits_integer, self.NUMBER_OF_DIGITS))
        # remove the latest from the list 
        self.number_permutations.remove(digits_integer) # like [(8, 6, 7), (7, 8, 6), (7, 6, 8), (6, 8, 7), (6, 7, 8)]
        print(f"DEBUG : remains permutations: {self.number_permutations}") 
        return "".join(str(c) for c in self.number_permutations[0]) # take the first one 

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
        if self.machine_input:
            return self.machine_guess()
            
        user_input = input(f"Guess # {counter} ==>:")
        try:
            if 999 < int(user_input) or int(user_input) < 100 or len(list(set(user_input))) != self.NUMBER_OF_DIGITS:
                raise ValueError
        except ValueError:
            print(f"You should enter {Bagles.NUMBER_OF_DIGITS}-digit number with the different digits")
            return None
        return user_input

    def coin_number(self, numbers = range(1,10)):
        first_digits = [i for i in numbers]
        shuffle(first_digits)
        return "".join(str(c) for c in first_digits[:self.NUMBER_OF_DIGITS])

# In order to run unittets run: python3 -m unittest bagles.py 
class BaglesTest(TestCase):
    def test_bagles_happy(self):
        bgl = Bagles(silent=True)
        bgl.get_user_input = Mock(return_value='123')
        type(bgl).hidden_number = PropertyMock(return_value="123")
        assert bgl.bagles() == True
       
    @patch('builtins.input', return_value='aaa')
    def test_bagles_unhappy(self, input):
        bgl = Bagles(silent=True)
        assert bgl.get_user_input() is None

    def test_bagles_unhappy2(self):
        bgl = Bagles(silent=True)
        bgl.get_user_input = Mock(return_value='124')
        type(bgl).hidden_number = PropertyMock(return_value="123")
        assert bgl.bagles() == False

    @patch('builtins.input', return_value='1444')
    def test_bagles_unhappy3(self, input):
        bgl = Bagles(silent=True)
        assert bgl.get_user_input() is None

    @patch('builtins.input', return_value='11')
    def test_bagles_unhappy4(self, input):
        bgl = Bagles(silent=True)
        assert bgl.get_user_input() is None    

    def test_guess1(self):
        bgl = Bagles(silent=True)
        type(bgl).hidden_number = PropertyMock(return_value="123")
        res=bgl.guess(user_input='124')
        assert res["Fermi"] == 2
        assert res["Bagles"] == False

    def test_guess2(self):
        bgl = Bagles(silent=True)
        type(bgl).hidden_number = PropertyMock(return_value="123")
        res=bgl.guess(user_input='312')
        assert res["Pico"] == 3
        assert res["Bagles"] == False    

    def test_guess3(self):
        bgl = Bagles(silent=True)
        type(bgl).hidden_number = PropertyMock(return_value="123")
        res=bgl.guess(user_input='321')
        assert res["Pico"] == 2
        assert res["Fermi"] == 1
        assert res["Bagles"] == False       

greeting = """
            I am thinking of a {}-digit number. Try to guess what it is.
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
    parser.add_argument('-n', dest='num_guesses', type=int, default=Bagles.GUESSES, required=False)
    parser.add_argument('-s', dest='silent',  action='store_true', default=False, required=False)
    parser.add_argument('-m', dest='machine_input',  action='store_true', default=False, required=False)
    return parser.parse_args()

# In order to run in machine mode 10 guesses: python3 bagles.py -n 10 -m
if __name__ == '__main__':
    args = parse()
    if not args.silent:
        print(greeting.format(Bagles.NUMBER_OF_DIGITS))
    Bagles(n_guesses=args.num_guesses, silent=args.silent, machine_input=args.machine_input).bagles()
   