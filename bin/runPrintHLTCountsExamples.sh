#!/bin/bash

set -x

## Columns in HLT Counts table
# Index : Column Name
# ------:-----------
# 1     : Name
# 2     : L1Pass
# 3     : PSPass
# 4     : PAccept

mkdir -p test_HLTCounts/

## example 1
# print all columns listed above
./printHLTCounts.py --lumiranges 326392,326499:32:44,326500 --pathnames HLT_HIGEDPhoton10_v1,HLT_HIGEDPhoton20_v1,HLT_HIGEDPhoton30_v1 &> test_HLTCounts/example1.log

## example 2
# print only the 1st and 4th column
./printHLTCounts.py --lumiranges 262640:87:102,263293:1:373,263322:64:1238 --pathnames HLT_HIPuAK4CaloJet40_Eta5p1_v1,HLT_HIPuAK4CaloJet60_Eta5p1_v1,HLT_HIPuAK4CaloJet80_Eta5p1_v1 --colIndex 1,4 &> test_HLTCounts/example2.log

## example 3
# HLT paths to search are in a txt file
# print all columns listed above
./printHLTCounts.py --lumiranges 326500:1:35,326501:1:294,326502:1:50,326503:1:32 --pathnames test_HLTCounts/HLTpaths.txt &> test_HLTCounts/example3.log

## example 4
# Lumi ranges are in a txt file
# HLT paths to search are in a txt file
# Save the output to a csv file
./printHLTCounts.py --lumiranges test_HLTCounts/lumiRanges.txt --pathnames test_HLTCounts/HLTpaths.txt --outcsv test_HLTCounts/example4.csv &> test_HLTCounts/example4.log

## example 5
# Lumi ranges are in a json file
# print all 4 columns, but change their order
# save the output to a csv file
# Change the order of columns
./printHLTCounts.py --lumiranges test_HLTCounts/lumiRanges.json --pathnames test_HLTCounts/HLTpaths.txt --colIndex 2,3,1,4 --outcsv test_HLTCounts/example5.csv &> test_HLTCounts/example5.log
