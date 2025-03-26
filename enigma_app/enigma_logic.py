import string

#Predefined rotors and reflectors

ROTORS = [
    "EKMFLGDQVZNTOWYHXUSPAIBRCJ0123456789",  # Rotor I
    "AJDKSIRUXBLHWTMCQGZNPYFVOE0123456789",  # Rotor II
    "BDFHJLCPRTXVZNYEIWGAKMUSQO0123456789",  # Rotor III
]

REFLECTOR = "YRUHQSLDPXNGOKMIEBFZCWVJAT0123456789"  # Adjusted Reflector

ALPHABET = string.ascii_uppercase + "0123456789"

class EnigmaMachine:
    def __init__(self,rotor_settings, reflector=REFLECTOR,plugboard=None):
        #We intialize the machine with the given rotor settings and the reflector
        self.rotors = [list(ROTORS[i]) for i in rotor_settings]
        self.reflector = list(reflector)
        self.plugboard =  self.create_plugboard(plugboard or {})

    def create_plugboard(self, swaps):
        #I created a plugboard for mapping letters
        plugboard = {letter:letter for letter in ALPHABET}
        for key, value in swaps.items():
            plugboard[key] = value
            plugboard[value] = key
        return plugboard
    
    def encrypt_letter(self, letter):
        #This function encrypts a single letter by passing through plugboard, rotors, reflector and back
        if letter not in ALPHABET:
            return letter #Ignoring no alphabetical characters
        
        #Step 1: Pass through the plugboard
        letter = self.plugboard[letter]

        #Step 2: Pass through the rotors (forward direction)
        for rotor in self.rotors:
            letter = ALPHABET[rotor.index(letter)]

        #Step 3: Pass through the reflector
        letter = self.reflector[ALPHABET.index(letter)]

        #Step 4: Pass through rotors(reverse direction)
        for rotor in reversed(self.rotors):
            letter = rotor[ALPHABET.index(letter)]

        #Step 5: Pass through plugboard again
        letter = self.plugboard[letter]
        return letter
    
    def encrypt_message(self,message):
        #Encrypts a full message letter by letter
        encryted_text = ''.join(self.encrypt_letter(letter) for letter in message.upper())
        return encryted_text
