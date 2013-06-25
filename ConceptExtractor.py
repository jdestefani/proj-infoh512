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
            wordsFile.write("Word\tPOS\tFrequency\n")
            statsFile = open(str(fileName + ".stats"), 'w+')
            statsFile.write("Length\tPolarity\tSubjectivity\tMood\n")
        except IOError as e:
            sys.stderr.write(e)
            sys.stderr.write("\n[ERROR] - Error in opening files!")
            sys.exit(2)
        relevantWords = {}
        relevantWords['verb'] = {}
        relevantWords['noun'] = {}
        relevantWords['adjective'] = {}
        relevantWords['adverb'] = {}

        print ("[STATUS] - Files " + fileName + ", " + str(fileName+".words") + ", " + str(fileName+".stats")  + " opened")

        print ("[STATUS] - Start processing " + fileName)
        for line in tweetsFile:
            #print line

            #NLTK Tokenization
            #for token in sent_tokenize(line):
                #for word in pos_tag(token):
                    #if word[1] in (u"NN", u"NNS", u"JJ"):
                        #if word[0] in relevantWords:
                            #relevantWords[word[0]] = relevantWords[word[0]] + 1
                        #else:
                            #relevantWords[word[0]] = 1

            #Line preprocessing
            for sentence in sent_tokenize(line):
                print sentence
                #Pattern Tokenization
                sentenceLine = parse(sentence, tokenize=True, lemmata=True, encoding='utf-8', light=True)
                statsFile.write( repr(len(line)) + "\t" + repr(polarity(line)) + "\t" + repr(subjectivity(line)) + "\t" + repr(mood(Sentence(sentenceLine))) + "\n")
                for tokenList in sentenceLine.split():
                    for token in tokenList:
                        # Token = [ Word, Tag, Chunk, PNP, Lemma ]

                        if not containsDigits(token[0]):
                            word = token[4]
                            if '"' in word:
                                word = word.replace('"', '')
                            if "'" in word:
                                word = word.replace("'", '')
                            if "." in word:
                                word = word.replace(".", '')

                            if token[1] in (u"NN", u"NNS", u"FW"):
                                if word in relevantWords['noun']:
                                    relevantWords['noun'][word] = relevantWords['noun'][word] + 1
                                else:
                                    relevantWords['noun'][word] = 1

                            if token[1] in (u"JJ", u"JJR", u"JJS"):
                                if word in relevantWords['adjective']:
                                    relevantWords['adjective'][word] = relevantWords['adjective'][word] + 1
                                else:
                                    relevantWords['adjective'][word] = 1

                            if token[1] in (u"VB", u"VBZ", u"VBP",u"VBD",u"VBN",u"VBG"):
                                if word in relevantWords['verb']:
                                    relevantWords['verb'][word] = relevantWords['verb'][word] + 1
                                else:
                                    relevantWords['verb'][word] = 1

                            if token[1] in (u"RB", u"RBR", u"RBS"):
                                if word in relevantWords['adverb']:
                                    relevantWords['adverb'][word] = relevantWords['adverb'][word] + 1
                                else:
                                    relevantWords['adverb'][word] = 1

        print ("[STATUS] - Flushing relevant words")

        print ("[STATUS] - Flushing NOUNS")
        for key, value in relevantWords['noun'].items():
            # NLTK Wordnet access
            synsets = wordnet.synsets( key , pos=wordnet.NOUN )
            if len(synsets) > 0:
                print "Root hypernyms:", synsets[0].root_hypernyms()

            # Get a collection of synsets (synonym sets) for a word
            #synsets = wordnet.synsets( key )
            ## Print the information
            #for synset in synsets:
                #print "-" * 10
                #print "Name:", synset.name
                #print "Lexical Type:", synset.lexname
                #print "Lemmas:", synset.lemma_names
                #print "Definition:", synset.definition
                #print "Hypernyms:", synset.hypernyms()
                #print "Hyponyms:", synset.hyponyms()
                #print "Member holonyms:", synset.member_holonyms()
                #print "Root hypernyms:", synset.root_hypernyms()
                #for example in synset.examples:
                    #print "Example:", example

            # Pattern Wordnet access
            #s = wordnet.synsets(Word(sentence=None, string=key))
            #if len(s) > 0:
                #print s[0].synonyms
            wordsFile.write(str(key) + "\t noun \t" + str(value) + "\n")

        print ("[STATUS] - Flushing ADJECTIVES")
        for key, value in relevantWords['adjective'].items():
            synsets = wordnet.synsets( key , pos=wordnet.ADJ )
            if len(synsets) > 0:
                print "Root hypernyms:", synsets[0].root_hypernyms()
            wordsFile.write(str(key) + "\t adjective \t" + str(value) + "\n")

        print ("[STATUS] - Flushing VERBS")
        for key, value in relevantWords['verb'].items():
            synsets = wordnet.synsets( key , pos=wordnet.VERB )
            if len(synsets) > 0:
                print "Root hypernyms:", synsets[0].root_hypernyms()
            wordsFile.write(str(key) + "\t verb \t" + str(value) + "\n")

        print ("[STATUS] - Flushing ADVERB")
        for key, value in relevantWords['adverb'].items():
            synsets = wordnet.synsets( key , pos=wordnet.ADV )
            if len(synsets) > 0:
                print "Root hypernyms:", synsets[0].root_hypernyms()
            wordsFile.write(str(key) + "\t adverb \t" + str(value) + "\n")


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
