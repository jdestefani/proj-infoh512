__authors__ = 'Jacopo De Stefani (jacopo.de.stefani@ulb.ac.be)\n    Nadine Khouzam (nadine.khouzam@ulb.ac.be)\n'

from pattern.en import polarity, subjectivity,mood
from pattern.en import parse, Sentence, Word
#from pattern.en import wordnet
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tag import pos_tag
from nltk.corpus import wordnet
from nltk.corpus import wordnet_ic
import sys
import re
import scipy.cluster.hierarchy
import matplotlib
from matplotlib.backends.backend_pdf import PdfPages
import numpy

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

                        if not ContainsDigits(token[0]):
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


        print ("[STATUS] - Performing clustering")

        print ("[STATUS] - Clustering NOUNS")
        nounList = FilterList(relevantWords['noun'].keys(), wordnet.NOUN)
        nounLinkageMatrix,nounClusters = PerformClustering(nounList, wordnet.NOUN)
        PlotDendrogram(str(fileName + ".cluster.noun"),"Nouns Dendrogram", nounList, nounLinkageMatrix)

        #print ("[STATUS] - Clustering ADJECTIVES")
        #adjectiveList = FilterList(relevantWords['adjective'].keys(),wordnet.ADJ)
        #adjectiveLinkageMatrix,adjectiveClusters = PerformClustering(adjectiveList, wordnet.ADJ)
        #PlotDendrogram(str(fileName + ".cluster.adj"),"Adjectives Dendrogram",adjectiveList, adjectiveLinkageMatrix)

        #print ("[STATUS] - Clustering VERBS")
        #verbList = FilterList(relevantWords['verb'].keys(), wordnet.VERB)
        #verbLinkageMatrix,verbClusters = PerformClustering(verbList, wordnet.VERB)
        #PlotDendrogram(str(fileName + ".cluster.verb"),"Verbs Dendrogram",verbList, verbLinkageMatrix)

        #print ("[STATUS] - Clustering ADVERBS")
        #adverbList = FilterList(relevantWords['adverb'].keys(), wordnet.ADV)
        #adverbLinkageMatrix,adverbClusters = PerformClustering(adverbList, wordnet.ADV)
        #PlotDendrogram(str(fileName + ".cluster.adv"),"Adverbs Dendrogram",adverbList, adverbLinkageMatrix)


        print ("[STATUS] - Flushing relevant words")

        print ("[STATUS] - Flushing NOUNS")
        for key, value in relevantWords['noun'].items():
            ## NLTK Wordnet access
            #synsets = wordnet.synsets( key , pos=wordnet.NOUN )
            #if len(synsets) > 0:
                #print "Root hypernyms:", synsets[0].root_hypernyms()

            wordsFile.write(str(key) + "\t noun \t" + str(value) + "\n")

        #print ("[STATUS] - Flushing ADJECTIVES")
        #for key, value in relevantWords['adjective'].items():
            #synsets = wordnet.synsets( key , pos=wordnet.ADJ )
            #if len(synsets) > 0:
                #print "Root hypernyms:", synsets[0].root_hypernyms()
            #wordsFile.write(str(key) + "\t adjective \t" + str(value) + "\n")

        #print ("[STATUS] - Flushing VERBS")
        #for key, value in relevantWords['verb'].items():
            #synsets = wordnet.synsets( key , pos=wordnet.VERB )
            #if len(synsets) > 0:
                #print "Root hypernyms:", synsets[0].root_hypernyms()
            #wordsFile.write(str(key) + "\t verb \t" + str(value) + "\n")

        #print ("[STATUS] - Flushing ADVERB")
        #for key, value in relevantWords['adverb'].items():
            #synsets = wordnet.synsets( key , pos=wordnet.ADV )
            #if len(synsets) > 0:
                #print "Root hypernyms:", synsets[0].root_hypernyms()
            #wordsFile.write(str(key) + "\t adverb \t" + str(value) + "\n")


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

def ContainsDigits(string):
    return bool(digitsRE.search(string))

def ComputeDistanceMatrix(wordList,pos):

    # Create distance matrix
    distanceMatrix = numpy.ndarray(shape=(len(wordList),len(wordList)), dtype=float, order='F')

    # Import information content
    #brown_ic = wordnet_ic.ic('ic-brown.dat')
    #semcor_ic = wordnet_ic.ic('ic-semcor.dat')

    # Compute pairwise distance according to different metrics
    for i in range(len(wordList)):
        synsets1 = wordnet.synsets( wordList[i] , pos=pos )
        if len(synsets1) > 0:
            synset1 = synsets1[0]
        else:
            synset1 = None

        for j in range(i):
            synsets2 = wordnet.synsets( wordList[i] , pos=pos )
            if len(synsets2) > 0:
                synset2 = synsets2[0]
            else:
                synset2 = None
            #Actual distance computation
            #if synset1 is None or synset2 is None:
                ##distanceMatrix[i,j] = numpy.inf
                #distanceMatrix[i,j] = 1.1
            #else:
            # Return a score denoting how similar two word senses are,
            # based on the shortest path that connects the senses in the is-a (hypernym/hypnoym) taxonomy.
            # The score is in the range 0 to 1, except in those cases where a path cannot be found
            # (will only be true for verbs as there are many distinct verb taxonomies), in which case -1 is returned.
            # A score of 1 represents identity i.e. comparing a sense with itself will return 1.
            #distanceMatrix[i,j] = synset1.path_similarity(synset2)

            # Leacock-Chodorow Similarity:
            # Return a score denoting how similar two word senses are, based on the shortest path
            # that connects the senses (as above) and the maximum depth of the taxonomy in which the senses occur.
            # The relationship is given as -log(p/2d) where p is the shortest path length and d the taxonomy depth.
            #distanceMatrix[i,j] = synset1.lch_similarity(synset2)


            # Wu-Palmer Similarity:
            # Return a score denoting how similar two word senses are,
            # Based on the depth of the two senses in the taxonomy and that of their Least Common Subsumer (most specific ancestor node).
            distanceMatrix[i,j] = synset1.wup_similarity(synset2)

            # Resnik Similarity:
            # Return a score denoting how similar two word senses are, based on the Information Content (IC) of the Least Common Subsumer (most specific ancestor node).
            # Note that for any similarity measure that uses information content, the result is dependent on the corpus
            # used to generate the information content and the specifics of how the information content was created.
            #distanceMatrix[i,j] = synset1.res_similarity(synset2, brown_ic)

            #Jiang-Conrath Similarity
            # Return a score denoting how similar two word senses are,
            # based on the Information Content (IC) of the Least Common Subsumer (most specific ancestor node) and
            # that of the two input Synsets.
            # The relationship is given by the equation 1 / (IC(s1) + IC(s2) - 2 * IC(lcs)).
            #distanceMatrix[i,j] = synset1.jcn_similarity(synset2, brown_ic)

            # Lin Similarity: Return a score denoting how similar two word senses are,
            # based on the Information Content (IC) of the Least Common Subsumer (most specific ancestor node)
            # and that of the two input Synsets.
            # The relationship is given by the equation 2 * IC(lcs) / (IC(s1) + IC(s2)).
            #distanceMatrix[i,j] = synset1.lin_similarity(synset2, brown_ic)

    return distanceMatrix

def PerformClustering(wordList,pos):
    clusters = {}
    # Compute distance matrix using wordnet similarity measures
    print ("[STATUS] - [CLUSTER] Computing distance matrix")
    distanceMatrix = ComputeDistanceMatrix(wordList,pos)
    # Performs hierarchical/agglomerative clustering on the given condensed distance matrix y
    print ("[STATUS] - [CLUSTER] Computing linkage matrix")
    #linkageMatrix = scipy.cluster.hierarchy.linkage(distanceMatrix, 'single')
    #linkageMatrix = scipy.cluster.hierarchy.linkage( distanceMatrix, 'complete' )
    #linkageMatrix = scipy.cluster.hierarchy.linkage( distanceMatrix, 'average' )
    #linkageMatrix = scipy.cluster.hierarchy.linkage( distanceMatrix, 'weighted' )
    #linkageMatrix = scipy.cluster.hierarchy.linkage( distanceMatrix, 'centroid' )
    linkageMatrix = scipy.cluster.hierarchy.linkage( distanceMatrix, 'ward')

    print linkageMatrix

    clusterLabels = scipy.cluster.hierarchy.fcluster(linkageMatrix, 20 , criterion='distance')
    for i in range(len(wordList)):
        if not clusters.has_key(clusterLabels[i]):
            clusters[clusterLabels[i]] = []
        clusters[clusterLabels[i]].append(wordList[i])

    print clusters
    #clusters = clusterlists(T)
    return linkageMatrix,clusters

def PlotDendrogram(filename,title,wordList,linkageMatrix):

    figure = matplotlib.pyplot.figure()
    figure.subplots_adjust(bottom=0.2)
    matplotlib.pyplot.ylabel('Distance')
    matplotlib.pyplot.title(title)
    scipy.cluster.hierarchy.dendrogram(linkageMatrix,
                                       color_threshold=1,
                                       labels=numpy.array(wordList),
                                       distance_sort='ascending',
                                       leaf_rotation=90)

    pp = PdfPages(str(filename) + '.pdf')
    pp.savefig(figure)
    pp.close()

def FilterList(wordList,pos):
    filteredList = []
    for word in wordList:
        synsets = wordnet.synsets(word, pos=pos)
        if len(synsets) > 0:
            filteredList.append(word)
    return filteredList

###############################################################################

#WORDNET INFORMATIONS

#Synset('entity.n.01')
#Synset('physical_entity.n.01')
#Synset('abstraction.n.06')
#Synset('thing.n.12')
#Synset('object.n.01')
#Synset('whole.n.02')
#Synset('congener.n.03')
#Synset('living_thing.n.01')
#Synset('organism.n.01')
#Synset('benthos.n.02')


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

###############################################################################
if __name__ == "__main__":
    main()
