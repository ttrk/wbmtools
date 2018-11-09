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

mkdir -p test_HLTSummary/

## example 1
# print all HLT summary columns for given comma separated list of paths
./printHLTSummary.py --run 326262 --pathnames HLT_HIGEDPhoton10_v1,HLT_HIGEDPhoton20_v1,HLT_HIGEDPhoton30_v1 &> test_HLTSummary/example1.log

## example 2
# print 2nd,5th, and 6th column from HLTSummary table
./printHLTSummary.py --run 263322 --pathnames HLT_HIPuAK4CaloJet40_Eta5p1_v1,HLT_HIPuAK4CaloJet60_Eta5p1_v1,HLT_HIPuAK4CaloJet80_Eta5p1_v1 --colIndex 2,4,5,6,7 &> test_HLTSummary/example2.log

## example 3
# HLT paths to search are in a txt file
# print first 6 columns from HLTSummary table
./printHLTSummary.py --run 326238 --pathnames test_HLTSummary/HLTpaths.txt --colIndex 1,2,3,4,5,6 &> test_HLTSummary/example3.log

## example 4
# HLT paths to search are in a txt file
# print first 7 columns from HLTSummary table
# save the output to a csv file
./printHLTSummary.py --run 326262 --pathnames test_HLTSummary/HLTpaths.txt --colIndex 1,2,3,4,5,6,7 --outcsv test_HLTSummary/example4.csv &> test_HLTSummary/example4.log

## example 5
# HLT paths to search are in a txt file
# print first 7 columns from HLTSummary table
# save the output to a csv file
# The two numbers following run number are min and max lumi sections
./printHLTSummary.py --run 326262:105:479 --pathnames test_HLTSummary/HLTpaths.txt --colIndex 1,2,3,4,5,6,7 --outcsv test_HLTSummary/example5.csv &> test_HLTSummary/example5.log
