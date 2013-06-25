#!/bin/bash

# $1 - Search query name

python2.7 TweetFetcher.py -s $1
python2.7 ConceptExtractor.py $1.filtered

echo "[STATUS] - Producing .pdf graphs"
Rscript ProcessStatistics.R $1.filtered.stats
