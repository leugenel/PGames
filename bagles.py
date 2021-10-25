from random import shuffle
from unittest.mock import Mock, patch, PropertyMock, MagicMock
from unittest import TestCase


class Bagles:

    GUESSES = 1
    NUMBER_OF_DIGITS = 3

    def __init__(self) -> None:
        first_digits = [i for i in range(1,10)]
        shuffle(first_digits)
        self.__hidden_number = "".join(str(c) for c in first_digits[:self.NUMBER_OF_DIGITS])
    
    @property
    def hidden_number(self):
        return self.__hidden_number

    def bagles(self):
        print("""
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
            You have 10 guesses to get it.""")

        print(self.hidden_number)

        for i in range(self.GUESSES):
            user_input = self.get_user_input(i)
            if not user_input:
                continue
            if user_input == self.hidden_number:
                print("Great you won! This is a number!")
                return
            bagles = True
            for i in range(self.NUMBER_OF_DIGITS):
                if user_input[i] == self.hidden_number[i]:
                    print("Fermi")
                    bagles = False
                    continue
                if user_input[i] in self.hidden_number:
                    print("Pico")
                    bagles = False  
                    continue
            if bagles:
                print("Bagles")

    @staticmethod
    def get_user_input(counter: int = 0) -> str:
        user_input = input(f"Guess # {counter} ==>:")
        try:
            if 999 < int(user_input) or int(user_input) < 99:
                raise ValueError
        except ValueError:
            print("You should enter 3-digit number")
            return None
        return user_input

class BaglesTest(TestCase):
    @patch('builtins.input', return_value='123')
    def test_bagles(self, input):
        # with patch('bagles.Bagles.hidden_number') as bmock:
        #     # instance = bmock.return_value
        #     # instance.number = "124"
        #     #bmock.return_value = "124"
        #     type(bmock.return_value).hidden_number = PropertyMock(return_value='123')
        #     binstance = Bagles
        #     print(bmock.hidden_number)
        #     print(binstance.hidden_number)
        #     print("end")
        bgl = Bagles()
        type(bgl).hidden_number = PropertyMock(return_value="124")
        bgl.bagles()
        # print(bgl.hidden_number)
        # assert bgl.hidden_number == "124", f"{bgl.hidden_number}"
        # Bagles = Mock()
        # Bagles.hidden_number.return_value = "124"
        # Bagles().bagles()
 

if __name__ == '__main__':
    #game = Bagles().bagles()
    BaglesTest().test_bagles()