#!bin/bash

# $1 - User screen name

python2.7 TweetFetcher.py -u $1
python2.7 ConceptExtractor.py $1.filtered
Rscript ProcessStatistics.R $1.filtered.stats
