#!/usr/bin/python

def wurv(word):
    scorefactor = 1
    probability = 1
    tilebag = TileBag()
    total = 0
    for t in tilebag.tile:
        total += tilebag.tile[t].freq
    word = model.Spelling(word)
    for tile in word.spelling:
        probability *= (1.00000*tile.freq/total)
        scorefactor *= word.score 
    return scorefactor * probability * probability

def prob(word):
    scorefactor = 1
    probability = 1
    tilebag = TileBag()
    total = 0
    for t in tilebag.tile:
        total += tilebag.tile[t].freq
    word = Spelling(word)
    for tile in word.spelling:
        probability *= (1.00000*tile.freq/total)
        scorefactor *= word.score 
    return probability
        
def replace_at(string,pos,letter):
    return string[:pos] + letter + string[pos+1:]

def uniqify(seq, idfun=None):  
    # http://www.peterbe.com/plog/uniqifiers-benchmark
    # order preserving
    if idfun is None:
        def idfun(x): return x
    seen = {}
    result = []
    for item in seq:
        marker = idfun(item)
        if marker in seen: continue
        seen[marker] = 1
        result.append(item)
    return result

def alloptions(word):
    tilebag = TileBag()
    p = 0
    drawn = {}
    necessary_blanks = {}
    ways_to_play = [word]

    # we record the number of each letter as we see it...
    for letter in word:
        # ...adding to that letter if we've seen it before...
        if drawn.has_key(letter):
            drawn[letter] +=1
            # ...and if we've seen more than exist in the bag...
            if drawn[letter] > tilebag.tile[letter].freq:
                # ...we increment another dict to count the necessary blanks.
                if necessary_blanks.has_key(letter):
                    necessary_blanks[letter] += 1
                    # ...while we're here, we add all possible locations of our necessary blanks to the pot
                    for w in ways_to_play:
                        index = 0
                        for l in w:
                            if letter == l:
                                ways_to_play.append(replace_at(w,index,"_"))
                            index += 1
                else:
                    necessary_blanks[letter] = 1
                    for w in ways_to_play:
                        index = 0
                        for l in w:
                            if letter == l:
                                ways_to_play.append(replace_at(w,index,"_"))
                            index += 1
        else:
            drawn[letter] = 1
    
    return uniqify(ways_to_play)

def getwurva(word):
    
    plays = alloptions(word)

    wurvi = [] # plural of wurv

    for p in plays:
        wurvi.append(wurv(p))

    result = 0
    for w in wurvi:
        result += w
    return result

def getprob(word):
    
    plays = alloptions(word)

    wurvi = [] # plural of wurv

    for p in plays:
        wurvi.append(prob(p))

    result = 0
    for w in wurvi:
        result += w
    return result

def contains(word,letter,count):
    #recursion!
    if count < 2:
        return word.find(letter) > -1
    else:
        found = word.find(letter)
        if found > -1:
            return contains(word[found+1:],letter,count-1)
        else:
            return False

def points(word,values):
    points = 0
    for letter in word:
        points += values[letter][2]
        #print letter + " is worth " + str(values[letter][1]) + "points. " + str(points)
        #print values[letter]
    return points
        
def calculate_prob(word,values):
    return 0

def hasletters(word,letters):
    for l in letters:
        if l in word:
            return True
    return False

def remove(word,letter):
    result = []
    found = False
    for l in word:
        if (l == letter) and (not(found)):
            found = True
        else:
            result.append(l)
    return ''.join(result)

def comprisedof(word,letters):
    out1 = letters
    tiles = letters.upper()
    for l in word:
        if l in tiles:
            print tiles
            tiles = remove(tiles,l)
            print "-> ",tiles
        else:
            return False
    print out1, tiles
    return True


def has(word,letters):
    result = True
    w = list(word)
    for l in letters.upper():
        if l in w:
            w = remove(w,l)
        else:
            return False
    return True

def hasallletters(word,letters):
    for l in letters:
        if l not in word:
            return False
    return True

def highscoring(word):
    return hasletters(word,['J','Q','X','Z'])

def midscoring(word):
    return hasletters(word,['F','H','K','V','W','Y'])

def generate_bag_list():
    bag = []
    data = open("tiles.txt","r")
    for line in data.readlines():
        line = line.rstrip()
        line = line.split()
        for i in range(0,int(line[1])):
            bag.append(line[0])
    return bag
   
def probability(word):
    p = 1.0000000
    drawn = {}
    count = 0
    for letter in word:
        if drawn.has_key(letter):
            p *= 1.000000*(tilebag.tile[letter].freq - drawn[letter])/(len(tilebag.tile) - count)
            #print "P * 1/",(tilebag.tile[letter].freq - drawn[letter])," = ",p
            drawn[letter] += 1
        else:
            p *= 1.000000*(tilebag.tile[letter].freq)/(len(tilebag.tile) - count)
            #print "P * 1/",tilebag.tile[letter].freq," = ",p
            drawn[letter] = 1
        count += 1

    return p

def board_score(spelling,placement):
    # word = "BUNNY"
    # squares = ['TW','__','__','DL','__']
    # values = [1,1,2,5...
    points = 0
    wordfactor = 1
    letterfactor = 1
    
    index = 0
    
    bingo_bonus = 0
    if len(spelling) > 6:
        bingo_bonus = 50
        
    for tile in spelling:
        if placement[index] == 'TL':
            points += tile.points * 3
        elif placement[index] == 'DL':
            points += tile.points * 2
        else:
            points += tile.points
            if placement[index] == 'TW':
                wordfactor *= 3
            elif placement[index] =='DW':
                wordfactor *= 2
        index += 1
    
    return points * wordfactor + bingo_bonus

def avg_board_score(spelling):
    board = [['TW','__','__','DL','__','__','__','TW','__','__','__','DL','__','__','TW'],
                 ['__','DW','__','__','__','TL','__','__','__','TL','__','__','__','DW','__'],
                 ['__','__','DW','__','__','__','DL','__','DL','__','__','__','DW','__','__'],
                 ['DL','__','__','DW','__','__','__','DL','__','__','__','DW','__','__','DL'],
                 ['__','__','__','__','DW','__','__','__','__','__','DW','__','__','__','__'],
                 ['__','TL','__','__','__','TL','__','__','__','TL','__','__','__','TL','__'],
                 ['__','__','DL','__','__','__','DL','__','DL','__','__','__','DL','__','__'],
                 ['TW','__','__','DL','__','__','__','DW','__','__','__','DL','__','__','TW'],
                 ['__','__','DL','__','__','__','DL','__','DL','__','__','__','DL','__','__'],
                 ['__','TL','__','__','__','TL','__','__','__','TL','__','__','__','TL','__'],
                 ['__','__','__','__','DW','__','__','__','__','__','DW','__','__','__','__'],
                 ['DL','__','__','DW','__','__','__','DL','__','__','__','DW','__','__','DL'],
                 ['__','__','DW','__','__','__','DL','__','DL','__','__','__','DW','__','__'],
                 ['__','DW','__','__','__','TL','__','__','__','TL','__','__','__','DW','__'],
                 ['TW','__','__','DL','__','__','__','TW','__','__','__','DL','__','__','TW']]
    scores = 0
    plays = 0
    for row in board:
        for position in range(0,len(row) - len(spelling) + 1):
            plays += 1
            placement = row[position:position+len(spelling)]
            scores += board_score(spelling,placement)
        
    return scores/plays

class Tile:
    
    def __init__(self,ltr,srt,frq,pts,vwl):
        self.letter = ltr # (str) the letter, i.e. "A"
        self.sort   = srt # (int) the alphabetical position, i.e. "1"
        self.freq   = frq # (int) the frequency this letter occurs, i.e. "9"
        self.points = pts # (int) the number of points this is worth, i.e. "1"
        self.vowel  = vwl

    def __str__(self):
        return '"'+self.letter+'" -> #'+str(self.sort)+' x'+str(self.freq)+ ' +'+str(self.points) + ' v'+str(self.vowel)

class TileBag:

    def __init__(self):
        self.tile = {}
        tileinfo = open("test/tiles.txt","r")
        order = 0
        for line in tileinfo.readlines():
            line = line.rstrip()
            line = line.split()
            self.tile[line[0]] = Tile(line[0],order,int(line[1]),int(line[2]),int(line[3]))
            order += 1

    def __str__(self):
        string = ''
        for k in self.tile.keys():
            string += "letter: "+ str(self.tile[k]) + "\n"
        return string


class Spelling: # string -> a list of ordered Tiles

    def __init__(self,word):
        self.word = word.strip()
        self.tilebag = TileBag()
        tiles = []
        for elem in self.word:
            tiles.append(self.tilebag.tile[elem])

        self.spelling = tiles

        self.score = avg_board_score(self.spelling)

    def __add__(self,other):
        return self.score+other.score

    def __str__(self):
        output = []
        output.append(self.word)
        output.append(str(len(self.word)))
        #output.append(str(self.spelling))
        output.append(str(getprob(self.word)))
        output.append(str(self.score))
        return "\t".join(output)

class Anagram:
    def add(x,y): return x+y

    def __init__(self,word):
        self.letters = letters
        self.words = words
        self.score = reduce(add, words)/len(words)
        

def test():
    bag = TileBag()
    print bag

#test()
