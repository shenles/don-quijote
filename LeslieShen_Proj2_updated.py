# -*- coding: cp1252 -*-
# Leslie Shen

## This program figures out what percent of vocab
## in Ch. 1-2 of "El ingenioso hidalgo don Quijote de la Mancha"
## is recognizable by someone who knows English but not much Spanish.

import re
import urllib

def trimQuijote(infile, outfile):
    '''Takes text file from Gutenberg and writes a file that has
    only the text of Chapters 1 through 2.
    INPUTS: infile(String) - original text file
            outfile(String) - output file to write to
    OUTPUTS: none'''

    # read infile
    myFile = open(infile,'r')
    myString = myFile.read()
    myFile.close()
    
    # Remove text above Ch 1. Search for line containing 'Primera parte del'.
    myMatch = re.search('\Primera\sparte\sdel\s.+\n', myString)
    if myMatch == None:
        print 'Error. No match found.'
        return
    myString = myString[myMatch.end(0):len(myString)]

    # Remove text below Ch 2. Search for 'III'.
    myMatch = re.search(r'(.*) III(\.*)', myString, re.M)
    if myMatch == None:
        print 'Error. No match found.'
        return
    myString = myString[0:myMatch.start(0)]

    # sub 3 or more consecutive newlines with only 2 newlines
    myString = re.sub('\n{3,}','\n\n',myString)
    
    # open outfile, write, and close.
    outFile = open(outfile,'w')
    outFile.write(myString)
    outFile.close()
    
    return

def getWebsterWords(letter, outputfile): # helper, called in makeEnglishDict
    '''Gets words only. Writes a file that has words separated by newlines.
    INPUTS: letter (String)- a letter (from A to Z, case insensitive)
            outputfile (String) - file to write to
    OUTPUTS: none'''

    letter = letter.lower()

    # fetch from URL
    url = 'http://www.mso.anu.edu.au/~ralph/OPTED/v003/wb1913_' + letter + '.html'
    myURLFile = urllib.urlopen(url)
    myString = myURLFile.read()
    myURLFile.close()

    # Open outputfile for APPENDING so entries for subsequent
    # letters are added on without overwriting previous letters.
    
    # WARNING: This tripped me up when I was testing. I realized
    # that each time I ran makeEnglishDict, the entire thing was
    # being added onto the bottom of the file again. So I have to
    # be careful to only ever run makeEnglishDict once.
    outFile = open(outputfile,'a')
    
    # entries are delimited by <P>...</P>
    myIter = re.finditer('<P>.*?</P>', myString)
    for line in myIter:

        myMatch = re.match('<P><B>(.*)</B>\s+\(<I>(.*)</I>\)\s+(.*)</P>',line.group(0))
        
        # write word to file
        outFile.write(myMatch.group(1) + '\n')
        
    outFile.close()
    
    return

def makeEnglishDict(newOutFile):
    '''Calls getWebsterWords for each of 20 desired letters (no W, X, U, K, Q, or Z).
   The result is a file of words; it will need to be trimmed and cleaned.
    INPUTS: newOutFile (String) - file to write to
    OUTPUTS: none'''
    ## Only run this ONCE, if at all.
    ## Also, this is slow. I've included the outfile, english_full.txt,
    ## so there's no need to run this. To prove it works, use the tester
    ## function testMakeDict (if desired).
    
    desiredLetters = 'abcdefghijlmnoprstuvy'
    
    for desired in desiredLetters:
        getWebsterWords(desired, newOutFile)

    return

def testMakeDict():
    '''Tests makeEnglishDict with fewer letters.'''

    ## remember, run this only once!
    
    wantedletters = 'abc'
    for wanted in wantedletters:
        getWebsterWords(wanted,'testfile_3.txt')
    return

def trimDict(unrulyFile, finalFile):
    '''Trims extraneous entries from the file of words.
    INPUTS: unrulyFile(String) - original file of words, english_full.txt
            finalFile(String) - output file to write to, english_trimmed.txt
    OUTPUTS: none'''

    ## This function is even slower than makeEnglishDict.
    ## The resulting file, english_trimmed.txt, is included in case you don't
    ## want to run this. Use the tester function to prove it works (if desired).
    
    # read unrulyFile
    myFile = open(unrulyFile,'r')
    myWords = myFile.read()
    myFile.close()

    # trim weird entries off top of file
    myMatch = re.search('Aam', myWords)
    if myMatch == None:
        print 'Error. No match found.'
        return
    myWords = myWords[myMatch.end(0):len(myWords)]

    # cleaning
    myWords = removePunct(myWords)
    myWords = myWords.lower()
    myWords = removeDuplicates(myWords)
    myWords = ' '.join(myWords)

    # open finalFile, write, close.
    trimmedFile = open(finalFile,'w')
    trimmedFile.write(myWords)
    trimmedFile.close()
    
    return

def testTrimDict():
    '''Tests trimDict with a smaller infile.'''
    trimDict('testfile1.txt','test2.txt')
    return

def removeDuplicates(wordstring):  # helper, called in trimDict and vocabQuijote
    '''Takes a string and removes duplicate words as well as
    very similar words - words starting with the same seven letters,
    and words that are in other words.
    INPUTS: somestring (String)
    OUTPUTS: myWordsList - list free of duplicates'''
    # Won't catch every single redundancy, but does reduce
    # situations like 'abdicated abdicating abdicate abdication' -
    # those words, though different, are sort of the same.
    # Also helps cut out things like 'yaul' and 'yaulp'.

    myWordsList = []
    stringsplit = wordstring.split()
    stringsplit.sort()
    current = stringsplit[1]
    previous = stringsplit[0]
    for index in range(1, len(stringsplit)):
        current = stringsplit[index]
        previous = stringsplit[index-1]
        if not current in myWordsList and not current[0:6] in previous and not current in previous:
            myWordsList.append(current)

    return myWordsList

duplicateTest = 'abdicable abdicant abdicated abdicating abdicate abdication abdicative abdicator abditive abditory abdomen abdominal abdominals abdominales abdominalia abdominoscopy abdominothoracic abdominous abduced abducing abduce abducted abducting abduct abduction abductor abeam abear abearance abearing abecedarian abecedary abed abegge abele abelian abelite abelonian abelmosk aberdevine aberr aberrance aberrancy aberrant aberrate aberration aberrational aberuncate aberuncator abetted abetting abet abetment abettal abetter abettor abevacuation abeyance abeyancy abeyant abhal abhominable abhominal abhorred abhorring abhor abhorrence abhorrency abhorrent abhorrently abhorrer abhorrible abib abidance abode abid abiding abide abider abidingly abies abietene abietic abietin abietine abietinic abietite abigail' 
accentTest = '-Sí oigo -respondió Sancho-; pero, ¿qué hace a nuestro propósito la caza de Roncesvalles? Así pudiera cantar el romance de Calaínos'

def replaceAccents(s):  # helper, called in vocabQuijote
    '''Replaces accented characters and other strange characters
    with a plainer alternative.
    INPUTS: s (String) - string that has accents, upside down question marks, etc.
    OUTPUTS: fresh (String) - string without those things'''

    ## Didn't originally plan on doing this, but sometimes when I opened
    ## Spanish files, these characters didn't display. Replacing them to be safe.

    # I had to look up a conversion chart
    chart = {0xc0:'A', 0xc1:'A', 0xc2:'A', 0xc3:'A', 0xc4:'A', 0xc7:'C',
        0xc8:'E', 0xc9:'E', 0xca:'E', 0xcb:'E',0xcc:'I', 0xcd:'I', 0xce:'I', 0xcf:'I',
        0xd1:'N',0xd2:'O', 0xd3:'O', 0xd4:'O', 0xd5:'O', 0xd6:'O', 0xd9:'U', 0xda:'U',
        0xdb:'U', 0xdc:'U',0xdd:'Y', 0xe0:'a', 0xe1:'a', 0xe2:'a',
        0xe3:'a', 0xe4:'a', 0xe6:'ae', 0xe7:'c', 0xe8:'e', 0xe9:'e', 0xea:'e',
        0xeb:'e',0xec:'i', 0xed:'i', 0xee:'i', 0xef:'i', 0xf0:'th', 0xf1:'n',
        0xf2:'o', 0xf3:'o', 0xf4:'o', 0xf5:'o', 0xf6:'o', 0xf8:'o',
        0xf9:'u', 0xfa:'u', 0xfb:'u', 0xfc:'u', 0xfd:'y', 0xff:'y', 0xa1:'!', 0xa8:'{umlaut}',
        0xad:'-', 0xaf:'_', 0xb4:"'", 0xbf:'?'}
    
    fresh = ''
    for i in s:
        if chart.has_key(ord(i)):
            fresh += chart[ord(i)]
        elif ord(i) >= 0x80:
            pass
        else:
            fresh += i
    return fresh

def removePunct(s):  # helper, called in vocabQuijote and trimDict
    '''Removes punctuation from string.
    INPUTS: s (String) - string to be cleaned
    OUTPUTS: newstring (String) - punctuationless string'''
    newstring =''
    for char in s:
        if(char==',' or char=='.' or char==';' or char==':'
           or char=='!' or char=='?' or char=='-' or char=='('
           or char==')' or char=='\''):
            newstring += ''
        else:
            newstring += char
    return newstring

def vocabQuijote(fileIn, fileOut):
    '''Takes in a filename - in our case the file that has the chunk
    of Don Quijote we got from trimQuijote() - and writes fileOut containing
    duplicate/accent/punctuation-free, lowercase vocabulary of filename.
    INPUTS: fileIn (string) - file being used, i.e. quijote_trimmed.txt
            fileOut (string) - quijotevocab.txt
    OUTPUTS: none'''

    # read fileIn
    myFile = open(fileIn)
    myWords = myFile.read()
    myFile.close()

    # cleaning
    myWords = replaceAccents(myWords)
    myWords = removePunct(myWords)
    myWords = myWords.lower()
    myWords = removeDuplicates(myWords)
    myWords = ' '.join(myWords)

    # write fileOut
    trimmedFile = open(fileOut,'w')
    trimmedFile.write(myWords)
    trimmedFile.close()

    return

def cognateCount(filename1, filename2, outfile):
    '''Takes the file that contains the cleaned English
    dictionary, and the file that contains the Quijote vocab,
    and for each word in the vocab, looks for a possible cognate in the dictionary.
    INPUTS: filename1, filename2 (Strings) - files to look in
            outfile (string) - file to write to
    OUTPUTS: integer'''

    ## This takes a while.

    dictFile = open(filename1)
    dictWords = dictFile.read()
    dictFile.close()

    vocabFile = open(filename2)
    vocabWords = vocabFile.read()
    vocabFile.close()

    # Make strings into lists.
    # Remove words shorter than 4 letters.
    vocabWords = vocabWords.split()
    dictWords = dictWords.split()
    vocabWords = [a for a in vocabWords if len(a) > 3]
    dictWords = [b for b in dictWords if len(b) > 3]

    cognateList = []
    
    for spanishword in vocabWords:
        # If a word is long enough and its substring appears in dictWords,
        # get a list of words in dictWords that start with the substring.
        # Remove duplicates.
        if len(spanishword) > 6:
            cogOne = spanishword[:5]
            r = re.compile('%s'%(cogOne))
            for engword in dictWords:
                if r.match(engword):
                    cognateList.append(engword)
    newcoglist = []
    for word in cognateList:
        if not word in newcoglist:
                newcoglist.append(word)
    newcogs = ' '.join(newcoglist)

    # write potential cognates to new file
    cognateFile = open(outfile,'w')
    cognateFile.write(newcogs)
    cognateFile.close()

    myFile = open(outfile)
    mycogs = myFile.read()
    myFile.close()
    mycogs.split()
    return len(mycogs)  # answer 6453

def testCognate():
    testercogs = cognateCount('english_trimmed.txt','testcog.txt','testcogs2.txt')
    return testercogs  # answer 1618

popular = ['hola','por favor','gracias','uno','dos','tres','cuatro','cinco','seis',
           'nada','amigo','amiga','adios','grande','bueno','buena','bajo','baja',
           'alto','alta','fresco','feliz','navidad','caliente','nombre',
           'madre','padre','mama','papa','hijo','hija','mucho','mucha','muy',
           'nada','yo','rojo','verde','camino','bien','me gusta','costa','rica',
           'rico','vida','loca','pronto','mi','casa','es','su','hombre','bella',
           'bonita','amor','agua','senor','senora','senorita','fiesta','siesta','tortilla',
           'sangria','muchos']

def commonWordsCount(inputlist, inputfile):  # helper, called in percents
    '''Takes a list of words and counts their occurrences in Ch 1-7 Don Quijote vocab.
    INPUTS: inputlist (list) - list of words, i.e. popular
            inputfile (string) - file to look in, i.e. quijote_vocab.txt
    OUTPUTS: integer'''

    # read inputfile
    myFile = open(inputfile)
    myWords = myFile.read()
    someWords = myWords.split()
    myFile.close()

    # Count how many popular words show up in string.
    counter = 0
    for word in popular:
        if word in myWords:
            counter += 1

    print 'In',len(someWords),'vocab words,',counter,'are common knowledge.'
    return counter  # answer is 36
    
def percents():
    '''Calculates the final numbers: what percent of the vocab in Don Quijote
    can be understood as cognates, and what percent can be understood because of
    mainstream knowledge.
    INPUTS: none
    OUTPUTS: two integers'''

    ## The cognate search is flawed, of course. In cognates.txt, a file of 6453
    ## supposed cognates, I estimate there are about 200 actually recognizable ones.
    ## 200.0/6453 = 0.0309933364326

    myFile = open('quijote_vocab.txt')
    myWords = myFile.read()
    someWords = myWords.split()
    myFile.close()
    
    totalvocab = len(someWords)
    # cognates = cognateCount('english_trimmed.txt','quijote_vocab.txt','cognates.txt')
    commonknowledge = commonWordsCount(popular, 'quijote_vocab.txt')
    # cognatepercent = ((cognates*0.0309933364)/totalvocab) * 100
    cognatepercent = 2.32315018921
    commonpercent = (float(commonknowledge)/totalvocab) * 100
    totalpercent = cognatepercent + commonpercent
    # print'In',totalvocab,'vocab words,',(cognates*0.0309933364),'are likely cognates.'
    print 'Cognates are',cognatepercent,'percent and popular words are',commonpercent,'percent of the vocabulary.' 
    print 'In total,',totalpercent,'percent of Ch 1-2 in Don Quijote might be understood.'
    return
