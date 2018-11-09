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

mkdir -p test_L1Summary/

## example 1
# print all L1 summary columns for given comma separated list of paths
./printL1Summary.py --run 326262 --pathnames L1_MinimumBiasHF1_AND_BptxAND,L1_SingleJet16_BptxAND,L1_SingleJet44_BptxAND &> test_L1Summary/example1.log

## example 2
# print 2nd,5th, and 6th column from L1Summary table
./printL1Summary.py --run 263322 --pathnames L1_ZeroBias,L1_MinimumBiasHF1_AND,L1_MinimumBiasHF2_AND --colIndex 2,5,6 &> test_L1Summary/example2.log

## example 3
# L1 paths to search are in a txt file
# print first 4 columns from L1Summary table
./printL1Summary.py --run 326238 --pathnames test_L1Summary/L1paths.txt --colIndex 1,2,3,4 &> test_L1Summary/example3.log

## example 4
# L1 paths to search are in a txt file
# print first 6 columns from L1Summary table
# save the output to a csv file
./printL1Summary.py --run 326262 --pathnames test_L1Summary/L1paths.txt --colIndex 1,2,3,4,5,6 --outcsv test_L1Summary/example4.csv &> test_L1Summary/example4.log

## example 5
# L1 paths to search are in a txt file
# print first 6 columns from L1Summary table
# save the output to a csv file
# The two numbers following run number are min and max lumi sections
./printL1Summary.py --run 326262:250:540 --pathnames test_L1Summary/L1paths.txt --colIndex 1,2,3,4,5,6 --outcsv test_L1Summary/example5.csv &> test_L1Summary/example5.log
