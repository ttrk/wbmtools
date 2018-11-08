#!/bin/bash

set -x

## Columns in L1 summary table
# Index : Column Name
# ------:-----------
# 1     : Bit
# 2     : Name
# 3     : Pre-DT Counts Before Prescale
# 4     : Pre-DT Rate Hz Before Prescale
# 5     : Pre-DT Counts After Prescale
# 6     : Pre-DT Rate Hz After Prescale
# 7     : Post-DT Counts From HLT
# 8     : Post-DT Rate Hz From HLT
# 9     : Initial Prescale
# 10    : Final Prescale
## WARNING : For older runs the column structure is different than newer ones. Example : index=5 points to "Pre-DT Counts After Prescale" for run 326238. The same index points to "Pre-DT RMS Rate, Hz After Prescale" for run 263322.

mkdir -p test/

## example 1
# print all L1 summary columns for given comma separated list of paths
./printL1Summary.py --run 326262 --pathnames L1_MinimumBiasHF1_AND_BptxAND,L1_SingleJet16_BptxAND,L1_SingleJet44_BptxAND &> test/example1.log

## example 2
# print 2nd,5th, and 6th column from L1Summary table
./printL1Summary.py --run 263322 --pathnames L1_ZeroBias,L1_MinimumBiasHF1_AND,L1_MinimumBiasHF2_AND --colIndex 2,5,6 &> test/example2.log

## example 3
# L1 paths to search are in a txt file
# print first 4 columns from L1Summary table
./printL1Summary.py --run 326238 --pathnames test/L1paths.txt --colIndex 1,2,3,4 &> test/example3.log

## example 4
# L1 paths to search are in a txt file
# print first 6 columns from L1Summary table
# save the output to a csv file
./printL1Summary.py --run 326262 --pathnames test/L1paths.txt --colIndex 1,2,3,4,5,6 --outcsv test/example4.csv &> test/example4.log
