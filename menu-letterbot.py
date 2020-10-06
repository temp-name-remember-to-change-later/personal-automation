#!/usr/bin/env python3
import random
import os
import pickle

# Note: This class uses user inputs for most of its functions, making it difficult to automate.
# To be honest this file is super over-engineered and for like 99% of its use cases the regular letterbot.py is both easier and more efficient.
# I originally thought all this pickling and save-state stuff would be necessary because the original letterbot implementation was so slow
# but the dictionary-based implementation is waaaay faster so this entire script is pretty unnecessary
# that said I don't wanna delete it
class MarkovTextBot:
    def __init__(self):
        self.usedtextarr = []
        self.textarr = []
        self.dic = {}
        self.depth = 1
        self.savepath = None
        self.active = True

    # Returns an list of tuples, consisting of n consecutive letters followed by the next letter, in order.
    def consecutive(self, n, text):
        arr = []
        for i in range(len(text) - n):
            arr.append((text[i:i+n], text[i + n]))
        return arr

    # Updates self.dic with the data from self.textarr
    def gendic(self):
        print('Generating dictionary... ', end='')
        text = '\n'.join(self.textarr)
        for line in self.textarr:
            self.usedtextarr.append(line)
        self.textarr = []
        keys = self.consecutive(self.depth, text)
        for key in keys:
            if key[0] not in self.dic:
                self.dic[key[0]] = [key[1]]
            else:
                self.dic[key[0]].append(key[1])
        print('Done')
        print()

    # Parses text to add to self.text.
    def parsetext(self):
        fname = input('Input filename, or leave blank for stdin: ')
        if fname == '':
            self.textarr.append(input("Input text: "))
            print()
        else:
            print('Parsing text... ', end='')
            f = open(fname)
            for line in f:
                self.textarr.append(line)
            print('Done')
            print()

    # Adds used texts back into new text pile:
    def reloadtexts(self):
        while self.usedtextarr != []:
            self.textarr.append(self.usedtextarr.pop())

    # Sets save path
    def setpath(self):
        fname = input('Input file path (.pkl): ')
        if os.path.isfile(fname):
            to_overwrite = input('File "{}" exists. Overwrite it? (y/N): '.format(fname))
            if to_overwrite.lower() != 'y':
                print('Aborting...')
                print()
                return
        self.savepath = fname
        print('File path set.')
        print()

    # Writes self to a pickle file. (probably inefficient space-wise but whatever it's easy and I have over 1tb of storage)
    def savestate(self):
        if self.savepath is None:
            print('Error: no save path set.')
            return False
        else:
            f = open(self.savepath, 'wb')
            print('Saving contents... ', end='')
            pickle.dump(self, f)
            print('Done')
            print()
            f.close()
            return True

    # Writes self.dic to a pickle file.
    def writefile(self):
        fname = input('Input file path of file to write to (.pkl): ')
        if os.path.isfile(fname):
            to_overwrite = input('File "{}" exists. Overwrite it? (y/N): '.format(fname))
            if to_overwrite.lower() != 'y':
                print('Aborting...')
                print()
                return
        f = open(fname, 'wb')
        print('Dumping contents... ', end='')
        pickle.dump(self.dic, f)
        print('Done')
        print()
        f.close()

    # Clears the terminal screen
    def clear_term(self):
        os.system('clear')

    # Shortens long dictionary entries by showing the first and last 5 entries.
    def dictentrytotext(self, key):
        val = self.dic[key]
        if len(val) <= 10:
            return '"{}": {}'.format(key, val)
        else:
            startval = val[:5]
            endval = val[len(val) - 5:]
            return '"{}": {}, ..., {}'.format(key, str(startval)[:len(str(startval)) - 1], str(endval)[1:])

    # Prints info of current bot.
    def summary(self):
        if self.usedtextarr == []:
            print('Used texts (length: 0): []')
        elif len(self.usedtextarr) <= 10:
            print('Used texts (length: {}):'.format(len(self.usedtextarr)))
            for text in self.usedtextarr:
                if len(text) <= 80:
                    print(text)
                else:
                    print('{} ... {}'.format(text[:40], text[len(text) - 40:]))
        else:
            print('Used texts (length: {}):'.format(len(self.usedtextarr)))
            for text in self.usedtextarr[:5]:
                if len(text) <= 80:
                    print(text)
                else:
                    print('{} ... {}'.format(text[:40], text[len(text) - 40:]))
            for text in self.usedtextarr[len(self.usedtextarr) - 5:]:
                if len(text) <= 80:
                    print(text)
                else:
                    print('{} ... {}'.format(text[:40], text[len(text) - 40:]))

        print()

        if self.textarr == []:
            print('Texts (length: 0): []')
        elif len(self.textarr) <= 10:
            print('Texts (length: {}):'.format(len(self.textarr)))
            for text in self.textarr:
                if len(text) <= 80:
                    print(text)
                else:
                    print('{} ... {}'.format(text[:40], text[len(text) - 40:]))
        else:
            print('Texts (length: {}):'.format(len(self.textarr)))
            for text in self.textarr[:5]:
                if len(text) <= 80:
                    print(text)
                else:
                    print('{} ... {}'.format(text[:40], text[len(text) - 40:]))
            for text in self.textarr[len(self.textarr) - 5:]:
                if len(text) <= 80:
                    print(text)
                else:
                    print('{} ... {}'.format(text[:40], text[len(text) - 40:]))
        print()

        if self.dic == {}:
            print('Dictionary (length: 0): {}')
        else:
            print('Dictionary (length: {}):'.format(len(self.dic)))
            keylist = list(self.dic.keys())
            if len(keylist) <= 20:
                for key in keylist:
                    print(self.dictentrytotext(key))
            else:
                for key in keylist[:5]:
                    print(self.dictentrytotext(key))
                print('...')
                for key in keylist[len(keylist) - 5:]:
                    print(self.dictentrytotext(key))

        print()
        print('Depth:', self.depth)
        print()

    # Dumps all info into either a file or stdout.
    def infodump(self):
        print('Compiling information... ', end='')
        
        arr = []
        if self.usedtextarr == []:
            arr.append('Used texts (length: 0): []')
        else:
            arr.append('Used texts (length: {}):'.format(len(self.usedtextarr)))
            for text in self.usedtextarr:
                arr.append(text)

        arr.append('')

        if self.textarr == []:
            arr.append('Texts (length: 0): []')
        else:
            arr.append('Texts (length: {}):'.format(len(self.textarr)))
            for text in self.textarr:
                arr.append(text)
        
        arr.append('')

        if self.dic == {}:
            arr.append('Dictionary (length: 0): {}')
        else:
            arr.append('Dictionary (length: {}):'.format(len(self.dic)))
            keylist = list(self.dic.keys())
            for key in keylist:
                arr.append('"{}": {}'.format(key, self.dic[key]))

        arr.append('')
        arr.append('Depth: {}'.format(self.depth))
        arr.append('')

        print('Done')

        fname = input('Enter file name to dump to (leave blank for stdout): ')
        if os.path.isfile(fname):
            over = input('File already exists. Overwrite? (y/N): ')
            if over.lower() != 'y':
                print('Aborting...')
                print()
                return

        if fname == '':
            for a in arr:
                print(a)
        else:
            f = open(fname, 'w')
            for a in arr:
                f.write(a)
                f.write('\n')
            f.close()
        print('Finished writing contents to {}'.format(fname))
        print()

    # Clears dictionary.
    def cleardic(self):
        self.dic = {}

    # Ends the session, prompting for a save.
    def endsession(self):
        tosave = input('Would you like to save before you exit? (y/n/C): ')
        if tosave.lower() == 'y':
            if self.savestate():
                print('Exiting...')
                print()
                self.active = False
            else:
                print('Error: Save failed. Please fix the error and try again.')
                print()
        elif tosave.lower() == 'n':
            print('Exiting...')
            print()
            self.active = False
        else:
            print('Invalid response. Aborting...')
            print()

    # Clears text.
    def cleartext(self):
        self.textarr = []

    # Sets depth of Markov chain (that is, the number of previous letters each new letter is based on.).
    # Also clears dictionary.
    def setdepth(self):
        if self.dic != {}:
            toclear = input('Changing the depth will clear the dictionary. Continue? (y/N): ')
            if toclear.lower() != 'y':
                print('Aborting...')
                print()
                return
            else: 
                self.dic = {}
        n = int(input('Enter an integer to set the depth of the Markov Chain: '))
        self.depth = n
        print()

    # Parses a dictionary and sets self.dic equal to it. Sets depth of chain to depth of dictionary if necessary.
    def parsedic(self):
        fname = input('Input filename of .pkl file: ')
        f = open(fname, 'rb')
        if self.dic != {}:
            toclear = input('Current dictionary is non-empty. Overwrite it? (y/N): ')
            if toclear.lower() != 'y':
                print('Aborting...')
                return
        print('Loading pickle file... ', end='')
        dic = pickle.load(f)
        if not isinstance(dic, dict):
            print()
            print('Error! File does not represent a dictionary. Aborting...')
            return
        print('Done')
        keys = list(dic.keys())
        n = len(keys[0])
        if n != self.depth:
            print('Note: Dictionary depth is {} != {}. Setting depth to {}.'.format(n, self.depth, n))
            self.depth = n
        self.dic = dic
        print()
        
    # Generates text based on dictionary.
    def gentext(self):
        textlength = int(input('Input desired length of text: '))
        seed = input('Input seed of length at least {} (leave blank for random seed): '.format(self.depth))
        keys = list(self.dic.keys())
        if seed == '':
            seed = random.choice(keys)
        elif len(seed) < self.depth or seed[len(seed) - self.depth:] not in keys:
            print('Seed not found in dictionary; using random seed instead.')
            seed = random.choice(keys)
        
        s = seed
        for i in range(textlength):
            s += random.choice(self.dic[s[len(s) - self.depth : len(s)]])
        
        print('Output:')
        print(s)
        print()

    # Loads a bot from a pickle file.
    def load(self):
        if self.usedtextarr != [] or self.textarr != [] or self.dic != {}:
            over = input('Doing this will overwrite the current session. Continue? (y/N): ')
            if over.lower() != 'y':
                return
        fname = input('Input file to load: ')
        f = open(fname, 'rb')
        pick = pickle.load(f)
        if self.__class__ != pick.__class__:
            print('Error: file is not a MarkovTextBot. Aborting...')
            print()
        else:
            self.usedtextarr = pick.usedtextarr
            self.textarr = pick.textarr
            self.dic = pick.dic
            self.depth = pick.depth
            self.savepath = fname
            print('Loaded file.')
            print()
        
    # Prints options.
    def helptext(self):
        print(
            'T: Parse text',
            'D: Parse dictionary file',
            'G: Updates current dictionary from text',
            'W: Write dictionary to file',
            'N: Set depth',
            'P: Set path to save to',
            'R: Reload used texts',
            'S: Save current state',
            'X: Generate text from dictionary',
            'C: Clear the terminal',
            'Q: End the session',
            'M: Print summary of bot info',
            'I: Dump unabridged bot info, with the option to save to a file',
            '?: Print this helptext',
            '',
        sep='\n')

    # Runs the TextBot.
    def run(self):
        options = {
                't': self.parsetext,
                'd': self.parsedic,
                'g': self.gendic,
                'w': self.writefile,
                'n': self.setdepth,
                'c': self.clear_term,
                'r': self.reloadtexts,
                'p': self.setpath,
                's': self.savestate,
                'l': self.load,
                'x': self.gentext,
                'q': self.endsession,
                'm': self.summary,
                'i': self.infodump,
                '?': self.helptext
            }
        self.active = True
        while self.active:
            try:
                choice = input("What would you like to do? (Enter ? for options): ")[0]
                func = options[choice.lower()]
            except:
                print('Error: Invalid choice.')
                print()
                continue

            try:
                func()
            except Exception as e:
                print('Caught exception:')
                print(e)
                print()

bot = MarkovTextBot()
bot.run()
