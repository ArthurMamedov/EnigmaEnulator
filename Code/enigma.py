from copy import copy
from sys import argv
from typing import List


class Enigma:
    def __init__(self, filepath = 'enigma.conf'):
        try:
            with open(filepath, 'r') as config:
                rotorconfs = config.readlines()
                self.__rotor1 = rotorconfs[0].replace(' \n', '').split(' ')
                self.__rotor2 = rotorconfs[1].replace(' \n', '').split(' ')
                self.__rotor3 = rotorconfs[2].replace(' \n', '').split(' ')
            print('Rotors initialized from "{}"'.format(filepath))
            self.__check_rotor(self.__rotor1)
            self.__check_rotor(self.__rotor2)
            self.__check_rotor(self.__rotor3)
        except FileNotFoundError:
            print('"{}" not found. Standard rotors are used.'.format(filepath))
            self.__rotor1 = [
                'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd',
                'f', 'g', 'h', 'j', 'k', 'l', 'z', 'x', 'c', 'v', 'b', 'n', 'm'
            ]
            self.__rotor2 = [
                'm', 'n', 'b', 'v', 'c', 'x', 'z', 'l', 'k', 'j', 'h', 'g', 'f',
                'd', 's', 'a', 'p', 'o', 'i', 'u', 'y', 't', 'r', 'e', 'w', 'q'
            ]
            self.__rotor3 = [
                'w', 'r', 'y', 'i', 'p', 'q', 'e', 't', 'u', 'o', 'a', 'd', 'g',
                'j', 'l', 's', 'f', 'h', 'k', 'x', 'v', 'n', 'z', 'c', 'b', 'm'
            ]


    def __rotate(self):
        def _rotate(rotor: list):
            elem = rotor.pop(0)
            rotor.append(elem)
        _rotate(self.__rotor1)
        if self.__rotor1[0] == 'q':
            _rotate(self.__rotor2)
            if self.__rotor2[0] == 'm':
                _rotate(self.__rotor3)


    def __reflect(self, letter):
        num = ord(letter)
        num = chr(ord('z') - num + ord('a'))
        res = chr(ord('a') + self.__rotor3.index(num))
        res = chr(ord('a') + self.__rotor2.index(res))
        res = chr(ord('a') + self.__rotor1.index(res))
        return res


    def __substitute(self, letter):
        result = ord(letter) - 97
        result = ord(self.__rotor1[result]) - 97
        result = ord(self.__rotor2[result]) - 97
        result = self.__rotor3[result]
        return result


    def __check_rotor(self, rotor: List[str]):
        if len(set(rotor)) != 26 or len(rotor) != 26:
            raise RuntimeError('Rotor alphabet size mismatch. It may have repeating letters or alphabet may be not completed.')
        for elem in rotor:
            if not elem.isalpha():
                raise RuntimeError('Only letters are allowed in rotor.')


    def __check_message(self, message: str):
        for l in message:
            if not l.isalpha():
                raise RuntimeError('You can only use letters! Neither numbers nor punctuation marks are not allowed.')


    def encrypt(self, message: str) -> str:
        message = message.lower().replace(' ', '')
        self.__check_message(message)
        encrypted = list()
        for l in message:
            s = self.__substitute(l)
            r = self.__reflect(s)
            self.__rotate()
            encrypted.append(r)
        return ''.join(encrypted).upper()


    def set_rotors(self, rotor1: list = None, rotor2: list = None, rotor3: list = None):
        if rotor1:
            self.__check_rotor(rotor1)
        if rotor2:
            self.__check_rotor(rotor2)
        if rotor3:
            self.__check_rotor(rotor3)
        if rotor1:
            self.__rotor1 = copy(rotor1)
        if rotor2:
            self.__rotor2 = copy(rotor2)
        if rotor3:
            self.__rotor3 = copy(rotor3)


    def get_rotor(self, num: int):
        if num == 1:
            return copy(self.__rotor1)
        elif num == 2:
            return copy(self.__rotor2)
        elif num == 3:
            return copy(self.__rotor3)
        else:
            raise RuntimeError('Wrong rotor number! Rotor number must be equal to 1, 2 or 3.')


def _fill_rotor(rotor, l):
    while True:
        t = input('ROTOR1[{}]: '.format(l))
        try:
            check(t, rotor)
            rotor.append(t)
            break
        except RuntimeError as err:
            print(err)


def check(data: str, src):
    if not data.isalpha():
        raise RuntimeError('Only letters are allowed. Neither numbers nor punctuation marks.')
    elif data in src:
        raise RuntimeError('You have already entered this letter.')
    elif len(data) != 1:
        raise RuntimeError('Only one letter needed.')


def init_rotors(filepath):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    rotor1 = list()
    rotor2 = list()
    rotor3 = list()
    with open(filepath, 'w') as config:
        print('\n ROTOR1 init:') 
        for l in alphabet:
            _fill_rotor(rotor1, l)
        print('\n ROTOR2 init:')
        for l in alphabet:
            _fill_rotor(rotor2, l)
        print('\n ROTOR3 init:')
        for l in alphabet:
            _fill_rotor(rotor3, l)
        config.write(' '.join([*rotor1, '\n']).lower())
        config.write(' '.join([*rotor2, '\n']).lower())
        config.write(' '.join([*rotor3, '\n']).lower())


def setup(enigma: Enigma):
    commands = ['exit', 'help', 'getrotors', 'setrotors']
    command, *args = input('Enter a command: ').lower().split()
    while len(args) != 2:
        args.append('')
    if command not in commands:
        print('Wrong command.')
        return
    if command == 'exit':
        exit()
    elif command == 'help':
        print('Help message... Year, it is THAT short and has SO little sence...')
    elif command == 'getrotors':
        if args[0] == 'write' and args[1]:
            with open(args[1], 'w') as file:
                file.write(' '.join([*enigma.get_rotor(1), '\n']))
                file.write(' '.join([*enigma.get_rotor(2), '\n']))
                file.write(' '.join([*enigma.get_rotor(3), '\n']))
        elif args[0] == 'write':
            with open('rotors.conf', 'w') as file:
                file.write(' '.join([*enigma.get_rotor(1), '\n']))
                file.write(' '.join([*enigma.get_rotor(2), '\n']))
                file.write(' '.join([*enigma.get_rotor(3), '\n']))
        elif args[0] == 'print' or not args[0]:
            for l in enigma.get_rotor(1):
                print(l, end=' ')
            print('')
            for l in enigma.get_rotor(2):
                print(l, end=' ')
            print('')
            for l in enigma.get_rotor(3):
                print(l, end=' ')
    elif command == 'setrotors':
        if args[0] == 'enter' or not args[0]:
            alphabet = 'abcdefghijklmnopqrstuvwxyz'
            rotor1 = list()
            rotor2 = list()
            rotor3 = list()
            print('\n ROTOR1 init:') 
            for l in alphabet:
                _fill_rotor(rotor1, l)
            print('\n ROTOR2 init:')
            for l in alphabet:
                _fill_rotor(rotor2, l)
            print('\n ROTOR3 init:')
            for l in alphabet:
                _fill_rotor(rotor3, l)
            enigma.set_rotors(rotor1, rotor2, rotor3)
        elif args[0] == 'read' and args[1]:
            with open(args[1], 'r') as config:
                rotorconfs = config.readlines()
                rotor1 = rotorconfs[0].replace(' \n', '').split(' ')
                rotor2 = rotorconfs[1].replace(' \n', '').split(' ')
                rotor3 = rotorconfs[2].replace(' \n', '').split(' ')
            print('Rotors initialized from "{}"'.format(args[1]))
            enigma.set_rotors(rotor1, rotor2, rotor3)
        elif args[0] == 'read':
            with open('rotors.conf', 'r') as config:
                rotorconfs = config.readlines()
                rotor1 = rotorconfs[0].replace(' \n', '').split(' ')
                rotor2 = rotorconfs[1].replace(' \n', '').split(' ')
                rotor3 = rotorconfs[2].replace(' \n', '').split(' ')
            print('Rotors initialized from "{}"'.format(args[1]))
            enigma.set_rotors(rotor1, rotor2, rotor3)


def encryption(enigma: Enigma):
    message = input('Enter your message: ')
    message = enigma.encrypt(message)
    print(message)


def start_enigma(filepath):
    try:
        enigma = Enigma(filepath)
        switcher = True
        while True:
            try:
                if switcher:
                    encryption(enigma)
                else:
                    setup(enigma)
            except KeyboardInterrupt:
                switcher = not switcher
            except Exception as ex:
                print(ex)

            # try:
            #     message = enigma.encrypt(message)
            #     print(message)
            # except RuntimeError as r:
            #     print(r)
            # except KeyboardInterrupt:
            #     print('Program finished.')
    except RuntimeError as re:
        print('Error: {}'.format(re))


def main():
    argvnum = len(argv)
    if argvnum == 1:
        print('Welcome to The Enigma Emulator!')
        print('There are 2 modes (the mode is set as command line arguments):')
        print('\t"init_rotors" - initialize the rotors used for encryption. If they are not set - standard used.')
        print('Third parameter - file, where to write. If not set, default name ("enigma.conf") if taken.')
        print('\t"start_enigma" - start Enigma in encryption mode.')
        print('Rotors can be initialized by passing .conf file as a second parameter to a program. if it is not set - standard used.')
        print('Example:\n\t> python enigma.py start_enigma rotors.conf')
        print('Means "start Enigma in encryption mode, take rotors from file "rotors.conf"')
        print('To close the program, press Ctrl + C')
        exit()
    if argv[1] == 'init_rotors' and argvnum < 4:
        init_rotors(argv[2] if len(argv) == 3 else 'enigma.conf')
    elif argv[1] == 'start_enigma' and argvnum < 4:
        start_enigma(argv[2] if len(argv) == 3 else 'enigma.conf')
    else:
        print('Unknown mode.')


if __name__ == '__main__':
    main()
