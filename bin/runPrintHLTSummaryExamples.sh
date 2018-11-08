#!/bin/bash

set -x

## Columns in HLT summary table
# Index : Column Name
# ------:-----------
# 1     : n
# 2     : Name
# 3     : nLS
# 4     : L1Pass
# 5     : PSPass
# 6     : PAccept
# 7     : RateHz
# 8     : PExcept
# 9     : PReject
# 10    : L1 Prerequisite

mkdir -p test/

## example 1
# print all L1 summary columns for given comma separated list of paths
./printHLTSummary.py --run 326262 --pathnames HLT_HIGEDPhoton10_v1,HLT_HIGEDPhoton20_v1,HLT_HIGEDPhoton30_v1 &> test/example1HLT.log

## example 2
# print 2nd,5th, and 6th column from HLTSummary table
./printHLTSummary.py --run 263322 --pathnames HLT_HIPuAK4CaloJet40_Eta5p1_v1,HLT_HIPuAK4CaloJet60_Eta5p1_v1,HLT_HIPuAK4CaloJet80_Eta5p1_v1 --colIndex 2,4,5,6,7 &> test/example2HLT.log

## example 3
# L1 paths to search are in a txt file
# print first 4 columns from HLTSummary table
./printHLTSummary.py --run 326238 --pathnames test/HLTpaths.txt --colIndex 1,2,3,4,5,6 &> test/example3HLT.log

## example 4
# L1 paths to search are in a txt file
# print first 6 columns from HLTSummary table
# save the output to a csv file
./printHLTSummary.py --run 326262 --pathnames test/HLTpaths.txt --colIndex 1,2,3,4,5,6,7 --outcsv test/example4HLT.csv &> test/example4HLT.log
