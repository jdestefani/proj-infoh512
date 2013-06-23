__authors__ = 'Jacopo De Stefani (jacopo.de.stefani@ulb.ac.be)\n    Nadine Khouzam (nadine.khouzam@ulb.ac.be)\n'

from pattern.en import polarity,subjectivity,mood
from pattern.en import parse, Sentence, Word
from pattern.en import wordnet
from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.tag import pos_tag
from nltk.corpus import wordnet
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
            wordsFile = open(str(fileName + ".words"), 'w+')
            wordsFile.write("Word\tFrequency\n")
            statsFile = open(str(fileName + ".stats"), 'w+')
            statsFile.write("Length\tPolarity\tSubjectivity\tMood\n")
        except IOError as e:
            sys.stderr.write(e)
            sys.stderr.write("\n[ERROR] - Error in opening files!")
            sys.exit(2)
        relevantWords = {}

        print ("[STATUS] - Files " + fileName + ", " + str(fileName+".words") + ", " + str(fileName+".stats")  + " opened")

        print ("[STATUS] - Start processing " + fileName)
        for line in tweetsFile:
            #print line

            #NLTK Tokenization
            for token in sent_tokenize(line):
                for word in pos_tag(token):
                    if word[1] in (u"NN", u"NNS", u"JJ"):
                        if word[0] in relevantWords:
                            relevantWords[word[0]] = relevantWords[word[0]] + 1
                        else:
                            relevantWords[word[0]] = 1

            #Pattern Tokenization
            #sentenceLine = parse(line, tokenize=True, lemmata=True, encoding='utf-8', light=True)
            #statsFile.write( len(line) + "\t" + repr(polarity(line)) + "\t" + repr(subjectivity(line)) + "\t" + repr(mood(Sentence(sentenceLine))) + "\n")
            #for sentence in sentenceLine.split():
                #for token in sentence:
                    ## Token = [ Word, Tag, Chunk, PNP, Lemma ]
                    #if token[1] in (u"NN", u"NNS", u"JJ"):
                        #word = token[4]
                        #if not containsDigits(word):
                            #if '"' in word:
                                #word = word.replace('"', '')
                            #if "'" in word:
                                #word = word.replace("'", '')
                            #if "." in word:
                                #word = word.replace(".", '')

                            #if word in relevantWords:
                                #relevantWords[word] = relevantWords[word] + 1
                            #else:
                                #relevantWords[word] = 1
            sys.exit()

        print ("[STATUS] - Flushing relevant words")
        for key, value in relevantWords.items():
            # NLTK Wordnet access
            # Get a collection of synsets (synonym sets) for a word
            synsets = wordnet.synsets( key )
            # Print the information
            for synset in synsets:
                print "-" * 10
            print "Name:", synset.name
            print "Lexical Type:", synset.lexname
            print "Lemmas:", synset.lemma_names
            print "Definition:", synset.definition
            print "Hypernyms:", synset.hypernyms()
            print "Hyponyms:", synset.hyponyms()
            print "Member holonyms:", synset.member_holonyms()
            print "Root hypernyms:", synset.root_hypernyms()
            for example in synset.examples:
                print "Example:", example

            # Pattern Wordnet access
            #s = wordnet.synsets(Word(sentence=None, string=key))
            #if len(s) > 0:
                #print s[0].synonyms
            wordsFile.write(str(key.encode('utf8')) + "\t" + str(value) + "\n")

        statsFile.close()
        wordsFile.close()
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
