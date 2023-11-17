import json


class Rotor:
    with open("src/configs.json", "r") as f:
        configs = json.load(f)

    def __init__(
        self,
        rotor_id: int,
        starting_position: str,
        offset=0,
        left_rotor=None,
        is_rightmost=False,
    ) -> None:
        """Initiate a rotor instance.

        Args:
            rotor_id (int): choose from 1, 2, 3, 4, and 5.
            starting_position (str): Set only letter for the value
            offset (int, optional): Chnage the position of the ring. Defaults to 0. Not larger than 26.
            left_rotor (_type_, optional): You must passing the left rotor if it has one rotor to its left. First rotor don't need this arg, because there is no rotor to its left. Subsequet rotor has to pass in its previous rotor.

        """
        if rotor_id not in [1, 2, 3, 4, 5]:
            raise ValueError(
                "Wrong rotor id. You should only choose one from 1, 2, 3, 4 and 5."
            )
        if offset > 26 or offset < 0:
            raise ValueError(
                "Wrong offset value. You should only set a value between 0 and 26."
            )
        if len(starting_position) != 1:
            raise ValueError(
                "Wrong starting postion. You should set only one letter for the starting position."
            )
        self.id = str(rotor_id)
        self.offset = offset
        self.left_rotor = left_rotor
        self.is_rightmost = is_rightmost
        self.position = starting_position.upper()
        self.notch = Rotor.configs["notch"][self.id]

    def encrypt_right_input(self, letter: str) -> str:
        """Encrypt a letter through a rotor. Turn the rotor after the encryption.

        Args:
            letter (str): Takes only one letter

        Raises:
            ValueError: If more than one letter is given

        Returns:
            str: Return a encrypted letter
        """
        if len(letter) != 1:
            raise ValueError("The rotor can only encrypt one letter each time.")
        is_lower = letter.islower()
        self.step()  # the rotor advances before the electrical signal runs through it.
        offset = Rotor.count_ring_offset(self.position)
        contacting_letter = Rotor.add_number_to_letter(letter.upper(), offset)
        if self.offset != 0:
            contacting_letter = Rotor.add_number_to_letter(
                contacting_letter, self.offset
            )
        output = Rotor.add_number_to_letter(
            Rotor.configs[self.id][contacting_letter], 26 - offset
        )
        if is_lower == True:
            return output.lower()
        return output

    def encrypt_left_input(self, letter: str) -> str:
        """Encrypt a letter that has been reflected by the reflector

        Args:
            letter (str): Takes only one letter

        Raises:
            ValueError: If more than one letter are given.

        Returns:
            str: Returns a letter that signifies the fixed position that contacts with the output pin.
        """
        if len(letter) != 1:
            raise ValueError("The rotor can only encrypt one letter each time.")
        is_lower = letter.islower()
        offset = Rotor.count_ring_offset(self.position)
        contacting_letter = Rotor.add_number_to_letter(letter.upper(), offset)
        if self.offset != 0:
            contacting_letter = Rotor.add_number_to_letter(
                contacting_letter, 26 - self.offset
            )
        output = list(
            filter(
                lambda x: Rotor.configs[self.id][x] == contacting_letter,
                Rotor.configs[self.id],
            )
        )[0]
        output = Rotor.add_number_to_letter(output, 26 - offset)
        if is_lower == True:
            return output.lower()
        return output

    def step(self) -> None:
        """Advance the rotor, i.e. change the current positon of the rotor by one letter. If it is the notch position, advance the rotor to the left as well."""
        if self.is_rightmost == True:
            self.position = Rotor.add_number_to_letter(self.position, 1)
        if self.notch == self.position and self.left_rotor != None:
            self.left_rotor.step()

    @property
    def position(self) -> str:
        return self._position

    @position.setter
    def position(self, value: str):
        self._position = value.upper()

    @staticmethod
    def letter_to_number(letter: str) -> int:
        """Change a letter into number so that it can be operated."""
        data = Rotor.configs["letter_to_number"]
        return data[letter.upper()]

    @staticmethod
    def number_to_letter(number: int) -> str:
        """Change a number between 1 to 26 into a corresponding letter between A and Z."""
        data = Rotor.configs["number_to_letter"]
        return data[str(number)]

    @staticmethod
    def add_number_to_letter(letter: str, number: int) -> str:
        """Add a number to a letter. For example, add 1 to A produces B

        Args:
            letter (str): A single letter
            number (int): An int between 0 and 26.

        Returns:
            str: Return a single letter.
        """
        if len(letter) != 1:
            raise ValueError("Takes only one letter each time.")
        letter = Rotor.letter_to_number(letter.upper())
        letter = number + letter
        if letter > 26:
            letter = letter % 26
        if letter % 26 == 0:
            letter = 26
        return Rotor.number_to_letter(letter)

    @staticmethod
    def count_ring_offset(position: str) -> int:
        return Rotor.letter_to_number(position) - Rotor.letter_to_number("A")


class Reflector:
    def __init__(self) -> None:
        """Initiate a reflector instance."""
        self.wiring = Rotor.configs["reflector"]

    def reflect(self, letter: str) -> str:
        """Reflect the input signal.

        Args:
            letter (str): Takes only on letter.

        Returns:
            str: Returns one letter
        """
        is_lower = letter.islower()
        if len(letter) != 1:
            raise ValueError("Takes only one letter each time.")
        output = self.wiring[letter.upper()]
        if is_lower == True:
            return output.lower()
        return output


class Plugboard:
    def __init__(self, *args: list) -> None:
        """A plugboard swaps pairs of two letters

        Raises:
            ValueError: If any of the given list does not have two items.
            ValueError: If any of the items in the lists is not a letter.
        """
        for l in args[0]:
            if len(l) != 2:
                raise ValueError("Takes lists that has exactly two letters")
            for i in l:
                if i.isalpha() == False:
                    raise ValueError("Items in your lists should be letters;")
        self.switch_pairs = args

    def switch(self, letter: str) -> str:
        """It Swaps the two letters. Given one, return another.

        Args:
            letter (str): Takes a single letter

        Returns:
            str: Return a single letter.
        """
        is_lower = letter.islower()
        for l in self.switch_pairs[0]:
            if letter.upper() in l:
                if l.index(letter.upper()) == 0:
                    output = l[1]
                if l.index(letter.upper()) == 1:
                    output = l[0]
                if is_lower == True:
                    return output.lower()
                else:
                    return output
            else:
                return letter


class Enigma:
    def __init__(
        self, rotors: tuple, plugboard: list, code: tuple, punctuation=True
    ) -> None:
        """It assemble all the parts into a enigma machine

        Args:
            rotors (tuple): tuple of rotor id, choose either 3 or 5 rotors from rotor ids 1, 2, 3, 4, and 5.
            plugboard (tuple): a tuple of lists; each list contains a pair of letters to be swap
            code (_type_, optional): a tuple of three-letter code
            punctuation (bool): default to Ture - every non-alphabetical character will be retain as is. False - they will be droped, and letters will be jammed togeter.

        """
        if len(rotors) != 3 and len(rotors) != 5:
            raise ValueError("Wrong number of rotors, either 3 or 5")
        if len(rotors) == 3:
            if len(code) != 3:
                raise ValueError(
                    "Need three letters for setting the machine cypher code"
                )
            for i in code:
                if i.isalpha() == False:
                    raise ValueError("Codes should be letters;")
            r1 = Rotor(rotors[0], code[0].upper())
            r2 = Rotor(rotors[1], code[1].upper(), left_rotor=r1)
            r3 = Rotor(rotors[2], code[2].upper(), left_rotor=r2, is_rightmost=True)
            self.rotors = [r3, r2, r1]
        if len(rotors) == 5:
            if len(code) != 5:
                raise ValueError(
                    "Need five letters for setting the machine cypher code"
                )
            for i in code:
                if i.isalpha() == False:
                    raise ValueError("Codes should be letters;")
            r1 = Rotor(rotors[0], code[0].upper())
            r2 = Rotor(rotors[1], code[1].upper(), left_rotor=r1)
            r3 = Rotor(rotors[2], code[2].upper(), left_rotor=r2)
            r4 = Rotor(rotors[3], code[3].upper(), left_rotor=r3)
            r5 = Rotor(rotors[4], code[4].upper(), left_rotor=r4, is_rightmost=True)
            self.rotors = [r5, r4, r3, r2, r1]
        self.reflector = Reflector()
        self.plgboard = Plugboard(plugboard)
        self.punctuation = punctuation

    def encrypt(self, char: str) -> str:
        """The whole process of encryption

        Args:
            letter (str): a single char

        Returns:
            str: a single letter, or the punctuations as is
        """
        if char.isalpha() == True:
            char = self.plgboard.switch(char)
            temp_list = list(i for i in range(len(self.rotors)))
            for i in temp_list:
                char = self.rotors[i].encrypt_right_input(char)
            char = self.reflector.reflect(char)
            temp_list.reverse()
            for i in temp_list:
                char = self.rotors[i].encrypt_left_input(char)
            char = self.plgboard.switch(char)
            return char
        else:
            if self.punctuation == True:
                return char
            else:
                return ""
