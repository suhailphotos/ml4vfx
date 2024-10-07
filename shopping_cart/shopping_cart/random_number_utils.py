import random
import string

class RandomUtils:
    """
    Class for generation of random numbers
    """
    @staticmethod
    def generate_random_id() -> str:
        """
        Generates a random ID number of length 6 as a string
        """
        return "".join(random.choices(string.ascii_uppercase, k=6))
