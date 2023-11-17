import argparse
from src.functions import Enigma
from rich.console import Console

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument(
    "-r",
    "--rotors",
    type=int,
    help="Chose either three or five rotors from 1, 2, 3, 4, and 5. Example: 【-r 123】",
)
parser.add_argument(
    "-p",
    "--plugboard",
    action="append",
    nargs="+",
    help="Pass in only a two-letter pair. Passing in only letter will raise a value error. If more than two letters are passed in, only the first two will be used as a plugboard pair. Use '-p' again to pass anohter pair. Example: 【-p ab】",
)
parser.add_argument(
    "-c",
    "--code",
    type=list,
    help="Pass in codes. Number of codes should match that of the rotots. Example: 【-c abc】",
)
parser.add_argument(
    "-po",
    "--punctuation_off",
    action="store_false",
    help="Punctuation mode. Default true. Pass in -po to turn it off.",
)
args = parser.parse_args()

# Check required args
for i in args.rotors, args.code:
    if not i:
        raise ValueError("Rotors and code are required. Please check help.")

# set rotors
rotors = tuple([int(i) for i in list(str(args.rotors))])

# Set plugboard
plugboard = []
if args.plugboard:
    for i in args.plugboard:
        plugboard.append(list(i[0][:2].upper()))
    for i in plugboard:
        if len(i) != 2:
            raise ValueError("Invalid args for plugboard. Please check help.")

# set code
code = tuple(args.code)
if len(code) != len(rotors):
    raise ValueError("Invalid args for code. Please check help.")
for i in code:
    if i.isalpha() == False:
        raise ValueError("Invalid args for code. Please check help.")

# set punctuation mode
punctuation = args.punctuation_off

# intiate the enigma machine
enigma = Enigma(rotors=rotors, plugboard=plugboard, code=code, punctuation=punctuation)

# user input
plaintxt = input("\nIn: ")
console = Console()
print("Out: ", end="")
for i in plaintxt:
    i = enigma.encrypt(i)
    console.print(i, end="", style="red")
print(f"\n")
