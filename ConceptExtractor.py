__authors__ = 'Jacopo De Stefani (jacopo.de.stefani@ulb.ac.be)\n    Nadine Khouzam (nadine.khouzam@ulb.ac.be)\n'

from pattern.en import polarity,subjectivity,mood
from pattern.en import parse, Sentence, Word
from pattern.en import wordnet
import sys
import re

digitsRE = _digits = re.compile('\d')

def main():
    print '''
    ###########################################################################
    #                            ConceptExtractor 1.0                         #
    ###########################################################################
    '''


    if len(sys.argv) == 1:
        usage()
        sys.exit(2)

    #Read files line by line
    for fileName in sys.argv[1:]:
        try:
            tweetsFile = open(fileName, 'r')
            outputFile = open(str(fileName + ".words"), 'w+')
            statsFile = open(str(fileName + ".stats"), 'w+')
            statsFile.write("Polarity\tSubjectivity\tMood\n")
        except IOError as e:
            sys.stderr.write(e)
            sys.stderr.write("\n[ERROR] - Error in opening files!")
            sys.exit(2)
        relevantWords = {}

        print ("[STATUS] - Files " + fileName + ", " + str(fileName+".words") + ", " + str(fileName+".stats")  + " opened")

        print ("[STATUS] - Start processing " + fileName)
        for line in tweetsFile:
            #print line
            sentenceLine = parse(line, tokenize=True, lemmata=True, encoding='utf-8', light=True)
            statsFile.write(repr(polarity(line)) + "\t" + repr(subjectivity(line)) + "\t" + repr(mood(Sentence(sentenceLine))) + "\n")
            for sentence in sentenceLine.split():
                for token in sentence:
                    # Token = [ Word, Tag, Chunk, PNP, Lemma ]
                    if token[1] in (u"NN", u"NNS", u"JJ"):
                        word = token[4]
                        if not containsDigits(word):
                            if '"' in word:
                                word = word.replace('"', '')
                            if "'" in word:
                                word = word.replace("'", '')
                            if "." in word:
                                word = word.replace(".", '')

                            if word in relevantWords:
                                relevantWords[word] = relevantWords[word] + 1
                            else:
                                relevantWords[word] = 1

        print ("[STATUS] - Flushing relevant words")
        for key, value in relevantWords.items():
            s = wordnet.synsets(Word(sentence=None, string=key))
            if len(s) > 0:
                print s[0].synonyms
            outputFile.write(str(key.encode('utf8')) + "," + str(value) + "\n")

        statsFile.close()
        outputFile.close()
        tweetsFile.close()


def usage():
    USAGE = '''Usage: ConceptExtractor [Files]

    Processes files containing tweets.

    This is free software, and you are welcome to redistribute it under certain conditions.
    See the GNU General Public License for details.
    There is NO warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

    AUTHORS:
    '''
    print(USAGE+__authors__)

def containsDigits(string):
    return bool(digitsRE.search(string))


if __name__ == "__main__":
    main()
