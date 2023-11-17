# PyEnigma
### Author: Luo Shuang
### Video Demo:  https://youtu.be/P0uK0RRerEw
### Description: A Python implementation of the Enigma machine.

#### What does PyEnigma do?
- It encrypts given plain text.
- It decrypts a cypher text with the machine settings used to encrypt it.

#### Command line usage
~~~ 
python enigma.py -r 123 -p ab -c abc -po
~~~ 
- [-r 123]: Choose roters 1, 2, and 3 from the list of the total five, 1, 2, 3, 4, and 5. Choose either three or five rotors.
- [-p ab]: Set plugboard to swap between a and b. More than one pairs can be set.
- [-c abc]: Set the starting positions of the rotors to be a, b, and c. The number of the codes has to be the same with that of the rotors.
- [-po]: Punctuation mode off. The mode is default to be on, meaning that every non-alphabetical characters will not be changed and there positions in the text will be retained.

#### Reference
1. Technical Details of the Enigma Machine, https://www.ciphermachinesandcryptology.com/en/enigmatech.htm#steppingmechanism
2. How did the Enigma Machine work? https://www.youtube.com/watch?v=ybkkiGtJmkM&t=823s